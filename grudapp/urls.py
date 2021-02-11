from django.conf.urls import url
from grudapp import views

urlpatterns =[
      
       url(r'^task/', views.task),
       url(r'^create_task', views.create_task),
       
       url(r'^update_task/(?P<pk>[0-9]+)$', views.update_task,name='update_task'),
       url(r'^detail_task/(?P<pk>[0-9]+)$', views.detail_task),
       url(r'^delate_task/(?P<pk>[0-9]+)$', views.delate_task,name='delate_task'),
]