
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import Like, Post, Posttest, User, Coach, Player, Scout, Zaakwaarnemer, Media
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

class ScoutSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    subject = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_scout = True
        if commit:
            user.save()
        scout = Scout.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), subject=self.cleaned_data.get('subject'))
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

class UserPlayerUpdateForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['user', 'followed_players', 'media_collection', 'posts']
    
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    club = forms.CharField(max_length=255, required=False)
    nft = forms.CharField(max_length=255, required=False)
    competition = forms.CharField(max_length=255, required=False)
    length = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
    preferred_leg = forms.CharField(max_length=10, required=False)
    position = forms.CharField(max_length=255, required=False)
    qualities = forms.CharField(max_length=255, required=False)
    career_statistics = forms.CharField(max_length=255, required=False)
    ambition = forms.CharField(widget=forms.Textarea, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_image = forms.ImageField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        self.fields['club'].initial = self.instance.club
        self.fields['nft'].initial = self.instance.nft
        self.fields['competition'].initial = self.instance.competition
        self.fields['length'].initial = self.instance.length
        self.fields['weight'].initial = self.instance.weight
        self.fields['preferred_leg'].initial = self.instance.preferred_leg
        self.fields['position'].initial = self.instance.position
        self.fields['qualities'].initial = self.instance.qualities
        self.fields['career_statistics'].initial = self.instance.career_statistics
        self.fields['ambition'].initial = self.instance.ambition
        self.fields['phone_number'].initial = self.instance.phone_number

    # def save(self, commit=True):
    #     player = super().save(commit=commit)
    #     user = player.user
    #     user.email = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.profile_image = self.cleaned_data['profile_image']
    #     print('aksjhdflkajsh;dfjkas;hdlkfh;aslkdf')
    #     print(self.cleaned_data['profile_image'])
    #     print(user.profile_image)
    #     user.save()
    #     return user
    
    def save(self, commit=True):
        player = super().save(commit=False)  # Save the player instance but don't commit yet
        user = player.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile_image = self.cleaned_data['profile_image']
        if commit:
            player.save()  # Save the player instance
            user.save()  # Save the user instance
        return player  # Return the player object



from django.forms import DateInput

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['last_login', 'groups', 'user_permissions', 'password', 'is_active', 'date_joined', 'is_player', 'is_coach', 'is_scout', 'is_staff', 'is_superuser', 'username', 'followed_users', 'following']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = DateInput(attrs={'type': 'date'})


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
        exclude = ['user', 'followed_players', 'media_collection', 'posts']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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






class PostFormTest(forms.ModelForm):
    class Meta:
        model = Posttest
        fields = ['text', 'image']














class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []