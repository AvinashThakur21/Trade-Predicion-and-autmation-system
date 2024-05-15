from django.urls import path
from . import views

# urlpatterns = [
#     path('',views.give_me_zone,name="give_me_zone"),
#     #path('room/',views.room,name="")
# ]



urlpatterns = [
    path('', views.give_me_zone, {'section': 'open'}, name='open_trades'),
    path('history/', views.give_me_zone, {'section': 'history'}, name='history_trades'),
    path('upcoming/', views.give_me_zone, {'section': 'upcoming'}, name='upcoming_trades'),
]