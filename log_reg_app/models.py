from django.db import models
from datetime import date, time, datetime, timedelta
import re, bcrypt

class UserManager(models.Manager):
    def addValidation(self, post_data):
        errors={}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        if post_data['birthday']:
            birthday = date.fromisoformat(post_data['birthday'])
            today_date = date.today()
            if birthday > today_date:
                errors['birthday'] = 'Birthday must be in the past.'
            else:
                delta = today_date - timedelta(weeks=676) # 13 * 52 weeks = 676
                if birthday > delta:
                    errors['birthday'] = 'User must be at least 13 years of age.'
        else:
            errors['birthday'] = 'Birthday must a valid date.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        else:
            if post_data['password'] != post_data['c_password']:
                errors['password'] = 'Passwords do not match!'
        return errors

    def loginValidation(self, post_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if not post_data['password']:
                errors['password'] = 'Password is missing!'
        else:
            user = User.objects.filter(email=post_data['email'])
            if not user:
                errors['user'] = 'This user does NOT exist in the database!'
            else:
                user = User.objects.get(email=post_data['email'])
                if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                    errors['password'] = 'WRONG Password!!!'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
