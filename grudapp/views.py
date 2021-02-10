from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound
from .serializers import TaskSerializers
from django.contrib.auth.decorators import permission_required

from .models import Task 
# Create your views here.
#DjangoModelPermissions

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task(req):
       tasks = Task.objects.all()
       serializers = TaskSerializers(tasks,many=True)
     
       return Response(serializers.data,status=status.HTTP_200_OK) 


@api_view(['POST'])
@permission_required('grudapp.add_task',)
def create_task(req):
      
       task = req.data.get('task',{})
       serializer = TaskSerializers(data=task)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data,status=status.HTTP_200_OK) 

@api_view(['PUT'])
@permission_required('grudapp.change_task', )
def update_task(req,pk):
       
       task = Task.objects.get(pk=pk)
       if task is None:
              
               raise NotFound('задача не найдена')
       
       if req.method == 'PUT':
              serializer = TaskSerializers(task,data=req.data.get('task'))
              serializer.is_valid(raise_exception=True)
              serializer.save()
              return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_required( 'grudapp.view_task', )
def detail_task(req,pk):
       
       task = Task.objects.get(pk=pk)
       if task is None:
               raise NotFound('задача не найдена')
       if req.method == 'GET':
              serializer = TaskSerializers(req.task)
              return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE',])
@permission_required( 'grudapp.delete_task', )
def delate_task(req,pk):
       
       task = Task.objects.get(pk=pk)
       if task is None:
               raise NotFound('задача не найдена')
       if req.method == 'DELETE':     
              task.delete()

              return Response({}, status=status.HTTP_200_OK)




             



              




