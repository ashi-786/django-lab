from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        username = request.POST.get('username').strip()
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            # if User.objects.filter(username__iexact=username):
            #     messages.warning(request, "Already Exists!")
            # else:
                messages.error(request, "Error creating account!")
    
    context = {'registerform': form}
    return render(request, "register.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid Credentials!")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")