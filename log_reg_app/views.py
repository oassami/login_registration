from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
    return render(request, 'index.html')

def user_register(request):
    request.session.clear()
    request.session['first_name']= request.POST['first_name']
    request.session['last_name']= request.POST['last_name']
    request.session['email']= request.POST['email']
    request.session['birthday']= request.POST['birthday']
    request.session['action']= 'register'
    errors = User.objects.addValidation(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], birthday=request.POST['birthday'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
    request.session['logged-in'] ="logged-in"
    return redirect('/success')

def user_login(request):
    request.session.clear()
    request.session['login_email'] = request.POST['email']
    request.session['action'] = 'login'
    errors = User.objects.loginValidation(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['first_name'] = user.first_name
    request.session['logged-in'] ="logged-in"
    return redirect('/success')

def user_seccess(request):
    if 'logged-in' not in request.session:
        return redirect('/clear_all')
    context = {
        'first_name': request.session['first_name'],
        'action': request.session['action'],
    }
    request.session.clear()
    return render(request, 'success.html', context)

def clear_forms(request):
    request.session.clear()
    return redirect('/')
