from django.urls import path, include
from . import views
#from ..version01 import urls
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), # login/
    path('logout/', views.logout_view, name='logout'),
    path('',include('version01.urls'),name='')
]
