from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('chat/<str:room_name>/', views.Room.as_view(), name='chat_room')
]
