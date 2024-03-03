
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Agent, Application, Like, Post, User, Coach, Player, Scout, Zaakwaarnemer, Media
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PlayerSignUpForm(UserCreationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Username'}))  # Add this line
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'label':'popo'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_player = True
        if commit:
            user.save()
        player = Player.objects.create(user=user)
        return user




class CoachSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, commit=True):
        print('kut kut kut kut kut kut kut')
        user = super().save(commit=False)
        user.is_coach = True
        if commit:
            user.save()
        coach = Coach.objects.create(user=user)
        return user

class AgentSignUpForm(UserCreationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Username'}))  # Add this line
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'label':'popo'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_scout = True
        if commit:
            user.save()
        agent = Agent.objects.create(user=user)
        return user

class ScoutSignUpForm(UserCreationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Username'}))  # Add this line
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'label':'popo'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_scout = True
        if commit:
            user.save()
        scout = Scout.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())






from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ['last_login', 'groups', 'user_permissions', 'password', 'is_active', 'date_joined', 'is_player', 'is_coach', 'is_scout', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class PlayerUpdateForm(UserChangeForm, forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['last_login', 'groups', 'user_permissions', 'password', 'is_active', 'date_joined', 'is_player', 'is_coach', 'is_scout', 'is_staff', 'is_superuser', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional customization to form fields if needed



from django.forms import DateInput

# Allbwani
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['last_login', 'groups', 'user_permissions', 'password', 'is_active', 'date_joined', 'is_player', 'is_coach', 'is_scout', 'is_staff', 'is_superuser', 'username', 'followed_users', 'following']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = DateInput(attrs={'type': 'date'})

from django import forms
from .models import Experience

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['club', 'user', 'from_date', 'to_date', 'position', 'description', 'club_image', 'place']
        required = {
            'to_date': False,
        }
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        # Add customizations or widgets if needed
        # For example, you can add a date picker widget for date fields:
        self.fields['from_date'].widget.attrs.update({'class': 'datepicker'})
        self.fields['to_date'].widget.attrs.update({'class': 'datepicker'})

class EditUserForm69(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            'is_player',
            'is_coach',
            'is_scout',
            'media_collection',
            'followed_users',
            'posts',
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = DateInput(attrs={'type': 'date'})

# Allbwani
class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['user', 'followed_players', 'media_collection', 'posts', 'nft', 'preferred_leg', 'career_statistics', 'ambition', 'phone_number']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        # self.fields['profile_image'].required = False


class ScoutProfileForm(forms.ModelForm):
    class Meta:
        model = Scout
        exclude = ['user', 'player_notes', 'posts']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        # self.fields['profile_image'].required = False
class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = ['user', 'player_notes', 'posts']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        # self.fields['profile_image'].required = False

class CoachProfileForm(forms.ModelForm):
    class Meta:
        model = Coach
        exclude = ['user', 'followed_players', 'media_collection', 'posts']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['profile_image'].required = False



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False












class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []



class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['clean_sheet', 'assists', 'goals', 'played_matches']





class PlayerGoalForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['goals']



class PlayerAssistForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['assists']


class PlayerCleanSheetForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['clean_sheet']


class PlayerPlayedMatchesForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['played_matches']


from .models import Vacancy

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'place']

# forms.py
from django import forms
from .models import Vacancy, Player



from django import forms

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['motivation']
