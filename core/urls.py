# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('create/', views.create_story_view, name='create_story'),
    path('story/<int:story_id>/', views.story_detail_view, name='story_detail'),
]
