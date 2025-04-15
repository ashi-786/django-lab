import os
from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from .models import PdfFile, History
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import fitz
from xhtml2pdf import pisa
import re
import uuid

# Create your views here.
@login_required
def index(request):
    return render(request, "user_dashboard/index.html")

@login_required
def history(request):
    return render(request, "user_dashboard/history.html")

@login_required
def get_files(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        if request.user.is_superuser:
            files = PdfFile.objects.filter(html_file__icontains=query).values()
        else:
            files = PdfFile.objects.filter(user=request.user, html_file__icontains=query).values()
    else:
        if request.user.is_superuser:
            files = PdfFile.objects.values()
        else:
            files = PdfFile.objects.filter(user=request.user).values()
    return JsonResponse(list(files), safe=False)

@login_required
def get_history(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        if request.user.is_superuser:
            history = History.objects.filter(html_file__icontains=query).values()
        else:
            history = History.objects.filter(user=request.user, html_file__icontains=query).values()
    else:
        if request.user.is_superuser:
            history = History.objects.values()
        else:
            history = History.objects.filter(user=request.user).values()
    return JsonResponse(list(history), safe=False)

@login_required
@csrf_exempt
def upload_pdf_file(request):
    if request.method == "POST":
        pdf_file_obj = request.FILES.get('pdf_file')
        if not pdf_file_obj:
            return JsonResponse({'status': False, 'msg': 'No PDF uploaded!'})
        
        if not pdf_file_obj.name.lower().endswith('.pdf'):
            return JsonResponse({'status': False, 'msg': 'Only PDF file allowed!'})
        
        filename = os.path.splitext(pdf_file_obj.name)[0]
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{filename}_{unique_id}"
        html_filename = f"{filename}.html"
        relative_html_path = str(Path('html_files') / html_filename)
        absolute_html_path = str(Path(settings.MEDIA_ROOT) / relative_html_path)
        # relative_html_path = os.path.join('html_files', html_filename)
        # absolute_html_path = os.path.join(settings.MEDIA_ROOT, 'html_files', html_filename)
        # print(absolute_html_path, relative_html_path)

        if PdfFile.objects.filter(user=request.user, html_file=relative_html_path).exists():
            return JsonResponse({'status': False, 'msg': "Already Exists!"})
        
        pdf = fitz.open(stream=pdf_file_obj.read(), filetype="pdf")
        html_content = ""
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text_html = page.get_text("html")
            html_content += f'<div data-page="{page_num + 1}">{text_html}</div>'
        pdf.close()

        with open(absolute_html_path, "w", encoding='utf-8') as fp:
            fp.write(html_content)

        if not os.path.exists(absolute_html_path):
            return JsonResponse({'status': 500, 'msg': "Error processing PDF!"})
        
        file = PdfFile.objects.create(user=request.user, html_file=relative_html_path)
        History.objects.create(user=request.user, file_fk=file, html_file=filename, status="Uploaded")
        return JsonResponse({'status': 200, 'msg': "PDF uploaded successfully!"})

@login_required
def file_editor(request):
    if not 'file_id' in request.GET:
        return redirect('index')
    
    file_id = request.GET.get('file_id')
    file = PdfFile.objects.get(pk = file_id)
    filename_with_ext = os.path.basename(file.html_file.name)  # "<filename>.html"
    filename = os.path.splitext(filename_with_ext)[0]
        
    absolute_html_path = Path(settings.MEDIA_ROOT) / str(file.html_file)

    if not os.path.exists(absolute_html_path):
        messages.error(request, 'File not found!')
        return redirect('index')
    
    with open(absolute_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    context = {'html_content': html_content, 'file_id': file_id, 'filename': filename,}
    return render(request, "user_dashboard/editor.html", context)


@login_required
@csrf_exempt  
def delete_data(request):
    if not 'file_id' in request.POST:
        return redirect('index')

    file_id = request.POST.get('file_id')
    file = PdfFile.objects.get(pk = file_id)
    file.delete()
    return JsonResponse({'status': 200, 'msg': "Pdf deleted successfully!"})

@login_required
@csrf_exempt  
def update_data(request):
    if request.method == "POST":
        if not 'file_id' in request.POST:
            return redirect('index')
        
        file_id = request.POST.get('file_id')
        html_content = request.POST.get('html_content')
        
        file = PdfFile.objects.get(pk = file_id)
        relative_path = str(file.html_file)
        filename_with_ext = os.path.basename(relative_path)
        filename = os.path.splitext(filename_with_ext)[0]
        absolute_path = Path(settings.MEDIA_ROOT) / relative_path

        with open(absolute_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # with open(absolute_path, 'r', encoding='utf-8') as f_read:
        #     saved_content = f_read.read()
        # if saved_content != html_content:
        #     return JsonResponse({'status': False, 'msg': 'Error updating file!'})
        
        History.objects.create(user=request.user, file_fk=file, html_file=filename, status="Edited")
        return JsonResponse({'status': 200, 'msg': "Pdf updated successfully!"})
        
@login_required
def download_pdf_file(request):
    if 'file_id' in request.GET:
        file_id = request.GET.get('file_id')
        file = PdfFile.objects.get(pk = file_id)
        absolute_path = os.path.join(settings.MEDIA_ROOT, file.html_file.name)

        if not os.path.exists(absolute_path):
            return JsonResponse({'status': False, 'msg': 'File not found!'})
        
        with open(absolute_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        # Generate PDF from HTML
        response = HttpResponse(content_type='application/pdf')
        filename = os.path.splitext(os.path.basename(file.html_file.name))[0] + ".pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        pisa_status = pisa.CreatePDF(html_content, dest=response)
        if pisa_status.err:
            return JsonResponse({'status': False, 'msg': f'Download Error: {str(pisa_status.err)}'})
        
        return response
    
@login_required
@csrf_exempt  
def rename_file(request):
    if request.method == "POST":
        if not 'file_id' in request.POST:
            return redirect('index')
        
        file_id = request.POST.get('file_id')
        html_file = request.POST.get('html_file').strip()
        if not file_id or not html_file:
            return JsonResponse({'status': False, 'msg': 'File name is required.'})

        if len(html_file) > 255:
            return JsonResponse({'status': False, 'msg': f'Filename too long!'})

        if re.search(r'[^\w\s\.\-\(\)\[\]\{\}\+\']|^[\-_]+|[\-_]+$', html_file):
            return JsonResponse({
                'status': False,
                'msg': 'Some characters are not allowed!\nTry a simpler filename!'
            })

        file = PdfFile.objects.get(pk=file_id, user=request.user)

        oldfile_with_ext = os.path.basename(file.html_file.name)
        base_name, _ = os.path.splitext(oldfile_with_ext)

        # new_base_name = slugify(html_file)  # Sanitize the filename [for special chars]
        new_html_filename = f"{html_file}.html"
        new_relative_path = str(Path('html_files') / new_html_filename)
        new_absolute_path = str(Path(settings.MEDIA_ROOT) / new_relative_path)
        status = f"{base_name} \nRenamed To \n{html_file}"
        # Check if the new filename already exists for this user
        if PdfFile.objects.filter(user=request.user, html_file=new_relative_path).exclude(pk=file_id).exists():
            return JsonResponse({'status': False, 'msg': 'Already exists!'})
        
        old_absolute_path = os.path.join(settings.MEDIA_ROOT, file.html_file.name)
        if not os.path.exists(old_absolute_path):
            return JsonResponse({'status': False, 'msg': 'File not found!'})

        old_absolute_path = str(Path(settings.MEDIA_ROOT) / file.html_file.name)
        os.rename(old_absolute_path, new_absolute_path)

        file.html_file = new_relative_path
        file.save()
        History.objects.create(user=request.user, file_fk=file, html_file=html_file, status=status)
        return JsonResponse({'status': 200, 'msg': 'File renamed successfully!', 'html_file': html_file})