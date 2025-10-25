from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import secrets

# store reset tokens temporarily
password_reset_tokens = {}


# REGISTER
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')


#  LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'accounts/login.html')


#  LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('/')


#  PASSWORD CHANGE
@login_required
def password_change_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('password_change')

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect!")
            return redirect('password_change')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  
        messages.success(request, "Password changed successfully!")
        return redirect('/')

    return render(request, 'accounts/password_change.html')


# PASSWORD RESET 
def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(16)
            password_reset_tokens[token] = user.username

            reset_link = f"http://127.0.0.1:8000/accounts/reset/{token}/"

            #  print link in console for demo  
            print("Password reset link:", reset_link)
 

            messages.success(request, "Password reset link sent! (Check console output)")
            return redirect('password_reset')
        except User.DoesNotExist:
            messages.error(request, "No account found with that email!")

    return render(request, 'accounts/password_reset.html')


#  PASSWORD RESET CONFIRM  
def password_reset_confirm_view(request, token):
    if token not in password_reset_tokens:
        messages.error(request, "Invalid or expired token!")
        return redirect('password_reset')

    username = password_reset_tokens[token]
    user = User.objects.get(username=username)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('password_reset_confirm', token=token)

        user.set_password(new_password)
        user.save()
        del password_reset_tokens[token]
        messages.success(request, "Password reset successful! Please login.")
        return redirect('login')

    return render(request, 'accounts/password_reset_confirm.html')
