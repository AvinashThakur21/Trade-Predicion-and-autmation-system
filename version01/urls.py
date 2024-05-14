from django.urls import path
from . import views

urlpatterns = [
    path('',views.give_me_zone,name="give_me_zone"),
    #path('room/',views.room,name="")
]