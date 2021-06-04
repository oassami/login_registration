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
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        else:
            # if User.objects.filter(email=post_data['email']):            This is s good way of doing it.... below is another way using TRY and EXCEPT
                # errors['email'] = "This email already exists!"
            try:
                self.get(email=post_data['email'])                  # try and get the record from database
                errors['email'] = "This email already exists!"      # it found one record in database
            except:
                pass                                                # did not find a record which what we need, so, do nothing and continue
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
        if not post_data['password']:
            errors['password'] = 'Password is missing!'
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
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
