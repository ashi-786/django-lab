from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
# from .forms import TodoForm

# import os
# from django import template
# register = template.Library()

# @register.filter
# def basename(path):
#     return os.path.basename(path)

def index(request):
    todos = Todo.objects.all()
    if request.method == "POST":
        name = request.POST.get('name').strip()
        status = request.POST.get('status')
        type = request.POST.get('type')
        todo_img = request.FILES.get('todo_img') if request.FILES.get('todo_img') else None
        file = request.FILES.get('file') if request.FILES.get('file') else None
        if Todo.objects.filter(name__iexact=name):
            messages.warning(request, "Already Exists!")
        else:
            Todo.objects.create(name=name, status=status, type=type, todo_img=todo_img, file=file)
            messages.success(request, "Todo created successfully!")
        return redirect('index')
    
    context = {'todos': todos}
    return render(request, 'index.html', context)

def update(request, pk):
    todo = Todo.objects.get(id = pk)
    if request.method == "POST":
        name = request.POST.get('name').strip()
        status = request.POST.get('status')
        type = request.POST.get('type')
        if request.FILES.get('todo_img'):
            todo.todo_img = request.FILES.get('todo_img') 
        if request.FILES.get('file'):
            todo.file = request.FILES.get('file')
        if Todo.objects.filter(name__iexact=name).exclude(id=pk):
            messages.warning(request, "Already Exists!")
        else:
            todo.name = name
            todo.status = status
            todo.type = type
            todo.save()
            # Todo.objects.filter(id=pk).update(name=name, status=status, type=type, todo_img=todo_img, file=file)
            messages.success(request, "Todo updated successfully!")
        return redirect('index')
    
    context = {'todo': todo}
    return render(request, 'update.html', context)

# def update(request, pk):
#     todo = Todo.objects.get(id = pk)
#     form = TodoForm(instance=todo)
#     if request.method == "POST":
#         form = TodoForm(request.POST, instance=todo)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
    
#     context = {'todo': todo, 'form': form}
#     return render(request, 'update.html', context)

def delete(request):
    tid = request.GET.get('id')
    todo = Todo.objects.get(id = tid)
    # todo = Todo.objects.get(id = pk)
    if request.method == "POST":
        todo.delete()
        messages.success(request, "Todo deleted successfully!")
        return redirect('index')
    
    context = {'todo': todo}
    return render(request, 'delete.html', context)