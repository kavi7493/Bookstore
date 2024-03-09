# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please try another email.")
            return redirect("register")

        if pass1 != pass2:
            messages.error(request, "Passwords did not match.")
            return redirect("register")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created. We have sent a confirmation email, please check.")

        # Email verification
        subject = 'Welcome to The Story Shop world'
        message = f'Hi {myuser.first_name}, thank you for registering in Story Shop world.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [myuser.email, ]
        send_mail(subject, message, email_from, recipient_list)

        return redirect("signin")

    return render(request, "reg.html")

@csrf_protect
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "main.html", {'fname': fname})
        else:
            messages.error(request, "Invalid credentials. Please try again or register.")
            return redirect('signin')

    return render(request, "signin.html")
    

def signout(request):
    logout(request)
    
    return redirect('home')