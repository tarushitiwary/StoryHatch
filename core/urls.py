from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile:view'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('story/create/', views.create_story_view, name='create_story'),
    path('story/<int:story_id>/add_chapter/', views.add_chapter_view, name='add_chapter'),
    path('story/<int:story_id>/', views.story_detail_view, name='story_detail'),
    path('', views.homepage_view, name='home'),
    path('my-stories/', views.my_stories_view, name='my_stories'),
    path('bookmark/<int:story_id>/', views.toggle_bookmark_view, name='toggle_bookmark'),
    path('search/', views.search_view, name='search'),

]
