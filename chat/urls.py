from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('chat/<str:room_name>/', views.Room.as_view(), name='chat_room')
]
