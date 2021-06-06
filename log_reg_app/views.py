from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


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
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'], 
        email = request.POST['email'], 
        birthday = request.POST['birthday'], 
        password = pw_hash
    )
    # messages.info(request, "You have created an account! Please log in...")             # This is good to have if you didn't auto logged in the user after registaring
    request.session['logged-in'] = "logged-in"
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

    # user = User.objects.filter(email=post_data['email'])                              # This all good programming, but below is a better way of doing it with TRY and EXCEPT.
    # if not user:
    #     errors['user'] = 'This user does NOT exist in the database!'
    # else:
    #     user = User.objects.get(email=post_data['email'])
    #     if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
    #         errors['password'] = 'WRONG Password!!!'

    try:
        user = User.objects.get(email = request.POST['email'])
        if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            messages.error(request, 'Incorrect email address or password.')
            return redirect('/')
    except:
        messages.error(request, 'Incorrect email address or password.')
        return redirect('/')
    request.session['first_name'] = user.first_name
    request.session['logged-in'] = "logged-in"
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

def pw_reset(request):
    if request.method == "POST":
        request.session.clear()
        errors = User.objects.resetValidation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/user/pw_reset')
        request.session['email'] = request.POST['email']
        request.session['password'] = request.POST['password']
        return redirect('/reseted')
    return render(request, 'reset.html')

def reseted(request):
    try:
        user = User.objects.get(email = request.session['email'])
    except:
        messages.error(request, 'email address not found.')
        return redirect('/user/pw_reset')
    pw_hash = bcrypt.hashpw(request.session['password'].encode(), bcrypt.gensalt()).decode()
    user.password = pw_hash
    user.save()
    request.session['action']= 'register'
    messages.info(request, "Reset successful...! Please log in...")  # This is good to have if you didn't auto logged in the user after registaring
    return redirect('/')
