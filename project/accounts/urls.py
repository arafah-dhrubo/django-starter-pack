from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name="login"),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
