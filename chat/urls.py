from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('chat', views.Chat.as_view(), name='chat'),
    path('find_friends/', views.FindFriends.as_view(), name='find_friends'),
    path('manage_profile/', views.ManageProfile.as_view(), name='manage_profile')
]
