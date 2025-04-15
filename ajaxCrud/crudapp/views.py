from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
from django.views.decorators.csrf import csrf_exempt  # For POST requests
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

def get_todo_data(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        todos = Todo.objects.filter(name__icontains=query).values()
    else:
        todos = Todo.objects.all().values()
    return JsonResponse(list(todos), safe=False)

@csrf_exempt
def save_data(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()
        status = request.POST.get('status')
        type = request.POST.get('type')
        todo_img = request.FILES.get('todo_img') if request.FILES.get('todo_img') else None
        file = request.FILES.get('file') if request.FILES.get('file') else None
        if Todo.objects.filter(name__iexact=name):
            return JsonResponse({'status': 0})
        else:
            Todo.objects.create(name=name, status=status, type=type, todo_img=todo_img, file=file)
            return JsonResponse({'status': 1})

@csrf_exempt
def delete_data(request):
    if 'tid' in request.POST:
        tid = request.POST.get('tid')
        todo = Todo.objects.get(pk = tid)
        todo.delete()
        return JsonResponse({'status': 1})
    else:
        return redirect('index')

@csrf_exempt
def get_edit_data(request):
    if 'tid' in request.POST:
        tid = request.POST.get('tid')
        todo = Todo.objects.get(pk = tid)
        data = {
            'id': todo.id,
            'name': todo.name,
            'status': todo.status,
            'type': todo.type,
            'todo_img': todo.todo_img.url if todo.todo_img else None,
            'file': todo.file.url if todo.file else None,
        }
        return JsonResponse(data)
    else:
        return redirect('index')

@csrf_exempt
def update_data(request):
    if 'id' in request.POST:
        tid = request.POST.get('id')
        todo = Todo.objects.get(pk = tid)
        if request.method == "POST":
            name = request.POST.get('name').strip()
            status = request.POST.get('status')
            type = request.POST.get('type')
            if request.FILES.get('todo_img'):
                todo.todo_img = request.FILES.get('todo_img') 
            if request.FILES.get('file'):
                todo.file = request.FILES.get('file')
            if Todo.objects.filter(name__iexact=name).exclude(pk=tid):
                return JsonResponse({'status': 0})
            else:
                todo.name = name
                todo.status = status
                todo.type = type
                todo.save()
                return JsonResponse({'status': 1})
    else:
        return redirect('index')