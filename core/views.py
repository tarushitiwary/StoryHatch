from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Story
from django.http import HttpResponse
from django.core.management import call_command

def run_migrations(request):
    call_command('makemigrations')
    call_command('migrate')
    return HttpResponse("Migrations applied.")  

def create_admin():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('home')
        else:
            messages.error(request, 'Please correct the form errors below.')  
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'core/login.html')

from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('login')


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    stories = Story.objects.filter(author=user)
    return render(request, 'accounts/profile.html', {'profile_user': user, 'stories': stories})


from .forms import ProfileEditForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the form errors below.')  
    else:
        form = ProfileEditForm(instance=profile, user=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .forms import StoryForm, ChapterForm
from .models import Story, Chapter

@login_required
def create_story_view(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            messages.success(request, "Your story has been published!")
            return redirect('story_detail', story_id=story.id)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = StoryForm()
    return render(request, 'core/create_story.html', {'form': form})

@login_required
def add_chapter_view(request, story_id):
    story = Story.objects.get(id=story_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.story = story
            chapter.created_by = request.user
            chapter.save()
            messages.success(request, "Chapter added!")
            return redirect('story_detail', story_id=story.id)
        else:
            messages.error(request, "Error adding chapter.")
    else:
        form = ChapterForm()
    return render(request, 'core/add_chapter.html', {'form': form, 'story': story})

def story_detail_view(request, story_id):
    story = Story.objects.get(id=story_id)
    chapters = story.chapters.order_by('chapter_number')  # related_name='chapters'
    return render(request, 'core/story_detail.html', {'story': story, 'chapters': chapters})

from django.db.models import Q

def homepage_view(request):
    create_admin()
    featured_stories = Story.objects.filter(is_featured=True)[:5]
    return render(request, "core/home.html", {"featured_stories": featured_stories})


@login_required
def my_stories_view(request):
    stories = Story.objects.filter(author=request.user)
    return render(request, 'core/my_stories.html', {'stories': stories})

@login_required
def toggle_bookmark_view(request, story_id):
    story = Story.objects.get(id=story_id)
    if request.user in story.bookmarks.all():
        story.bookmarks.remove(request.user)
        messages.info(request, "Removed from bookmarks.")
    else:
        story.bookmarks.add(request.user)
        messages.success(request, "Bookmarked!")
    return redirect('story_detail', story_id=story.id)

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Story.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query)
        ).filter(is_public=True)
    return render(request, 'core/search.html', {'results': results, 'query': query})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or your homepage
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})
