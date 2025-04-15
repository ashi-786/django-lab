from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        User = get_user_model()  # Get custom User model
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': False, 'msg': 'Email already exists!'})
        # if password != password2:
        #     return JsonResponse({'status': False, 'msg': 'Passwords do not match'})
        
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')# Log in user immediately
        return JsonResponse({'status': 200, 'msg': "Signup Successful!"})

    return render(request, "user_accounts/signup.html")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            return JsonResponse({'status': 401, 'msg': 'Invalid Credentials!'})
        
        login(request, user)
        return JsonResponse({'status': 200, 'msg': 'Login successful!'})
        # return redirect('index')

    return render(request, "user_accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required()
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        post_data = request.POST
        old_password = post_data.get("old_password")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        User = get_user_model()  # Get custom User model
        user = User.objects.get(email= request.user.email)
        if not user.check_password(old_password):
            return JsonResponse({'status': False, 'msg': 'Wrong Old Password!'})
        
        if password != password2:
            return JsonResponse({'status': False, 'msg': 'Passwords do not match'})
        
        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({'status': 200, 'msg': 'Password changed successfuly!'}, status=200)

    return render(request, "user_accounts/change_password.html")

@login_required()
@csrf_exempt
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        ppic = request.FILES.get('ppic')

        user.first_name = first_name
        user.last_name = last_name

        if ppic:
            # Delete old ppic
            if user.ppic:
                if os.path.isfile(user.ppic.path):
                    os.remove(user.ppic.path)
            user.ppic = ppic

        user.save()
        return JsonResponse({'status': 200, 'msg': 'Profile updated successfully!'})
    return render(request, "user_accounts/user_profile.html")