from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import CharField
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

class RegisterationSerializer(serializers.ModelSerializer):
       password = serializers.CharField(max_length=128,
              min_length=8,
              write_only=True)

       token = serializers.CharField(max_length =255,
              read_only=True)
             
       class Meta:
              model = User
              fields = ['email','password', 'token']

       def create(self, validated_data):
              
           return User.objects.create_user(**validated_data)




class LoginSerializer(serializers.Serializer):
       
       email = serializers.CharField(max_length = 255)
       password = serializers.CharField(max_length=255,
              write_only=True)
       token =serializers.CharField(max_length = 255,
              read_only = True)
       roles =serializers.CharField(max_length = 255,
              read_only = True)       
       
       def validate(self, data):

              email = data.get('email',None)
              password = data.get('password',None)

              if email is None:
                     raise serializers.ValidationError('Укажите email!')
                     
              if  password is None:
                            raise serializers.ValidationError('Укажите пароль!')

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.  
              user = authenticate(username=email,
                     password=password)
              
              if user is None :
                     raise serializers.ValidationError('Неправильный пользователь или пароль!')

              if not user.is_active:
                     raise serializers.ValidationError('пользователь был удален!')
              
              return {
                     "email":user.email,
                     "roles" :[ x.name for x in Group.objects.filter(user=user)],
                     "token":user.token
              }

class UserSerializer(serializers.ModelSerializer):
       
       password = serializers.CharField(max_length=128,min_length=8,write_only= True)
       

       class Meta(object):
              model = User
              fields = ('token','email', 'password')

              read_only_fields = ("token",)
       
       def update(self, instance, validated_data):
           
              password = validated_data.pop("password",None)

              for key,value in validated_data.items():
                     setattr(instance,key,value)

              if password is not None:
                     instance.set_password(password)
              
              instance.save()

              return instance
