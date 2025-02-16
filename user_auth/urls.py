from django.urls import path
from . import views


# Namespace for user authentication-related URLs.
app_name = 'user_auth'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('authenticate_user/', views.authenticate_user,
         name='authenticate_user'),
    path('show_user/', views.show_user, name='show_user'),
    path('register/', views.register, name='register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    ]
