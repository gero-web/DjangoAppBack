from __future__ import unicode_literals
import datetime
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,BaseUserManager
)

import jwt
from django.conf import settings
from datetime import datetime,timedelta
from django.contrib.auth.models import Group

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
       
        if not email:
            raise ValueError('Email is not!')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                
                group = Group.objects.get(name='user_task')
                user.groups.add(group)
               
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

        
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self) -> str:
        return self.email
        
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
       
        token = jwt.encode({
            "id":self.pk,
            "email":self.email,
           
           
         },
         settings.SECRET_KEY,algorithm = "HS256")
        
        return token.decode('utf-8')

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self