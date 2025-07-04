from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Secure password hashing
        if commit:
            user.save()
            # Create profile with bio and avatar
            Profile.objects.create(
                user=user,
                bio=self.cleaned_data['bio'],
                avatar=self.cleaned_data.get('avatar')
            )
        return user
    from django.contrib.auth.models import User

class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Accept user instance
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email
        self.user = user

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
            profile.save()
        return profile
    
from .models import Story, Chapter
from django import forms

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'summary', 'is_public']
        
class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['content', 'chapter_number', 'parent_chapter']
