from django.conf.urls import url 
from backend import views

urlpatterns = [
 
         url(r'^register/', views.RegisterationApiView.as_view()),
         url(r'^login/', views.LoginAPIView.as_view()),
         url(r'^profile/', views.UserRetrieveUpdateAPIView.as_view()),
        

]