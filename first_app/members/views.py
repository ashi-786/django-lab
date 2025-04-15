from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def members(request):
    allmembers = Member.objects.all().values()
    context = {'allmembers': allmembers,}
    # template = loader.get_template('all_members.html')
    # return HttpResponse(template.render(context, request))
    return render(request, "all_members.html", context)

@login_required(login_url='login')
def details(request, slug):
    allmembers = Member.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {'allmembers': allmembers,}
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def index(request):
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    return render(request, "index.html")

def testing(request):
    data = Member.objects.all().order_by('fname').values()
    template = loader.get_template('template.html')
    context = {'allmembers': data}
    return HttpResponse(template.render(context, request))
