from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import views as auth_views
from .decorators import coach_required, player_required, scout_required

from .forms import AgentProfileForm, AgentSignUpForm, PlayerAssistForm, PlayerCleanSheetForm, PlayerGoalForm, PlayerPlayedMatchesForm, PlayerSignUpForm, CoachSignUpForm, LoginForm, PlayerStatsForm, ScoutSignUpForm, EditProfileForm, PlayerProfileForm, ScoutProfileForm, CoachProfileForm, VacancyForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

User = get_user_model()
from django.contrib.auth import login

# def player_registration(request):
#     if request.method == 'POST':
#         form = PlayerRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Log in the user
#             return redirect('login')  # Redirect to the home page after successful registration
#     else:
#         form = PlayerRegistrationForm()
#     return render(request, 'registration/player_registration.html', {'form': form})

from .models import Application, Experience, Player, Post, Vacancy

def home(request):
    return render(request, 'home.html')
def landing(request):
    return render(request, 'social/landing.html')

from .forms import PostForm  # Import the PostForm
from .forms import MediaForm  # Import the MediaForm




from django.utils.timesince import timesince

@login_required
def feed(request):
    form = PostForm(request.POST, request.FILES)
    mediaform= MediaForm(request.POST, request.FILES)

    if request.method == 'POST':
        # Handle the form submission for creating a new post
        if form.is_valid() and mediaform.is_valid():
            print(form.cleaned_data)
            print(mediaform.cleaned_data)
            if form.cleaned_data['text'] is not '' or mediaform.cleaned_data['file'] is not None:
                new_post = form.save(commit=False)
                
                # Set the user field to the currently logged-in user
                new_post.user = request.user
                # new_post.media.set(request.FILES)
                # Now save the Post instance with the user association
                new_post.save()
                media_instance = mediaform.save(commit=False)
                media_instance.post = new_post  # Associate the media with the newly created post
                media_instance.save()  # Save the media instance
                # form.save()
                return redirect('feed')  # Redirect to the feed after a successful post submission

            else:
                print("niet goed")

        else:
            print('not valid')
            print(form.errors)
            print(mediaform.errors)


    posts = Post.objects.all()
    posts_with_duration = []
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)


    for post in posts:
        # Calculate the duration since the post was created
        duration = timesince(post.created_at)
        posts_with_duration.append((post, duration))

    posts_with_comments = []
    for post, duration in posts_with_duration:
        # Fetch comments for the current post
        comments = Comment.objects.filter(post=post)
        posts_with_comments.append((post, duration, comments))


    users = User.objects.all()
    
    return render(request, 'theme/index.html', {'posts': posts_with_comments, 'form':form, 'mediaform':mediaform, 'users':users, 'liked_posts':liked_posts})







from django.utils.decorators import method_decorator

class PlayerSignUpView(CreateView):
    model = User
    form_class = PlayerSignUpForm
    template_name = 'accounts/player_signup.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is logged in
        if self.request.user.is_authenticated:
            return redirect('feed')
        else:
            # User is not logged in, proceed with the normal behavior
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'player'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('edit_account')


    def form_invalid(self, form):
        # Print the form errors to the console
        print('invaliddddddd')
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Form validation error in field '{field}': {error}")
        # return HttpResponse(status=400)
        return render(self.request, self.template_name, {'form': form})


# class CoachSignUpView(CreateView):
#     model = User
#     form_class = CoachSignUpForm
#     template_name = 'coaches/coach_signup.html'
#     print('kopkop')

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'coach'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('coach-home')




class ScoutSignUpView(CreateView):
    model = User
    form_class = ScoutSignUpForm
    template_name = 'accounts/scout_signup.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is logged in
        if self.request.user.is_authenticated:
            return redirect('feed')
        else:
            # User is not logged in, proceed with the normal behavior
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'scout'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('edit_account_scout')


    def form_invalid(self, form):
        # Print the form errors to the console
        print('invaliddddddd')
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Form validation error in field '{field}': {error}")
        # return HttpResponse(status=400)
        return render(self.request, self.template_name, {'form': form})




class AgentSignUpView(CreateView):
    model = User
    form_class = AgentSignUpForm
    template_name = 'accounts/agent_signup.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is logged in
        if self.request.user.is_authenticated:
            return redirect('feed')
        else:
            # User is not logged in, proceed with the normal behavior
            return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'scout'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('edit_account_agent')


    def form_invalid(self, form):
        # Print the form errors to the console
        print('invaliddddddd')
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Form validation error in field '{field}': {error}")
        # return HttpResponse(status=400)
        return render(self.request, self.template_name, {'form': form})




class ScoutSignUpView2(CreateView):
    model = User
    form_class = ScoutSignUpForm
    template_name = 'scouts/scout_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'scout'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('scout-home')




class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    template_name = 'social/login.html'
    redirect_authenticated_user = True
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            print('pooooooo')
            # if user.is_player:
            #     print('is_player')
            #     return reverse('feed')
            # elif user.is_coach:
            #     print('is_coach')
            #     return reverse('player_list')
            # elif user.is_scout:
            #     print('is_scout')
            #     return reverse('player_list')
            return reverse('feed')
            
        else:
            return reverse('login')
    def form_invalid(self, form):
        # Print the form errors to the console
        print('invaliddddddd')
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Form validation error in field '{field}': {error}")
        # return HttpResponse(status=400)
        return render(self.request, self.template_name, {'form': form})

@login_required
@player_required
def player_home(request):
    return render(request, 'players/player_home.html')


@login_required
@scout_required
def scout_home(request):
    return render(request, 'scouts/scout_home.html')


@login_required
@coach_required
def coach_home(request):

    return render(request, 'coaches/coach_home.html')






from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, PlayerUpdateForm

@login_required
def update_user(request):
    if request.method == 'POST':
        form = PlayerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('player-profile')  # Replace 'profile' with the URL name of the user's profile page
    else:
        form = PlayerUpdateForm(instance=request.user)
    return render(request, 'update_user.html', {'form': form})

# noallbwani
# @login_required
# def player_profile(request):
#     player = request.user.player  # Assuming the player instance is associated with the user
#     if request.method == 'POST':
#         form = UserPlayerUpdateForm(request.POST, request.FILES, instance=player)
#         if form.is_valid():
#             form.save()
#             # Redirect or do something else
#     else:
#         form = UserPlayerUpdateForm(instance=player)  # Pass the player instance to the form

#     return render(request, 'update_user.html', {'form': form, 'player': player})






def player_list(request):
    players = Player.objects.all()
    return render(request, 'players/player_list.html', {'players': players})

def player_detail(request, player_pk):
    player = get_object_or_404(Player, username=player_pk)
    return render(request, 'players/player_detail.html', {'player': player})













# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         print('request.method == post')
#         form = EditProfileForm(request.POST, request.FILES, instance=request.user)
#         profile_form = PlayerProfileForm(request.POST, instance=request.user.player)  # request.FILES is show the selected image or file

#         print("request.FILES")
#         print("request.FILES")
#         print("request.FILES")
#         print(request.FILES)
#         if form.is_valid() and profile_form.is_valid():
#             user_form = form.save()
#             custom_form = profile_form.save(False)
#             custom_form.user = user_form
#             custom_form.save()
#             return redirect('player_list')
#         else:
#             print('Error kut')
#             print(form.errors)

#             print('profile_form kut')
#             print(profile_form.errors)
#             # form = EditProfileForm(instance=request.user)
#             # profile_form = PlayerProfileForm(instance=request.user.player)

#             return render(request, 'accounts/edit_profile.html', {'form': form, 'profile_form': profile_form})

#             # return render(request, 'your_template.html', {'form': form, 'profile_form': profile_form})

#     else:
#         form = EditProfileForm(instance=request.user)


#         player = getattr(request.user, 'player', None)
        
#         if player is not None:
#             profile_form = PlayerProfileForm(instance=request.user.player)
#             print("player is not None")

#         scout = getattr(request.user, 'scout', None)

#         if scout is not None:
#             print("scout is not None")
#             profile_form = ScoutProfileForm(instance=request.user.scout)

#         coach = getattr(request.user, 'coach', None)


#         if coach is not None:
#             print("coach is not None")
#             profile_form = CoachProfileForm(instance=request.user.coach)

#         # if request.user.player is not None:
#         #     profile_form = PlayerProfileForm(instance=request.user.player)
            

#         # if request.user.coach:
#         #     profile_form = ProfileForm(instance=request.user.coach)
            
#         # if request.user.scout:
#         #     profile_form = ProfileForm(instance=request.user.scout)
            
#         # profile_form = PlayerProfileForm(instance=request.user.coach)
#         args = {}
#         # args.update(csrf(request))
#         args['form'] = form
#         args['profile_form'] = profile_form
        
#         return render(request, 'accounts/edit_profile.html', args)





from .forms import EditUserForm69
@login_required
def edit_account_player(request):
    if request.method == 'POST':
        print('request.method == post')
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = PlayerProfileForm(request.POST, instance=request.user.player)  # request.FILES is show the selected image or file

        print("request.FILES")
        print(request.FILES)
        if form.is_valid() and profile_form.is_valid():
            print("form.is_valid")

            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            # return redirect('player_list')
            success = True
            return render(request, 'theme/edit_account_player.html', {'form': form, 'profile_form': profile_form, 'success': success})

        else:
            print('Error kut')
            print(form.errors)

            print('profile_form kut')
            print(profile_form.errors)
            # form = EditProfileForm(instance=request.user)
            # profile_form = PlayerProfileForm(instance=request.user.player)

            return render(request, 'theme/edit_account_player.html', {'form': form, 'profile_form': profile_form})

            # return render(request, 'your_template.html', {'form': form, 'profile_form': profile_form})

    else:
        args = {}

        # form = EditProfileForm(instance=request.user)
        # # form = EditUserForm69(instance=request.user)

        # player = getattr(request.user, 'player', None)
        # if player is not None:
        #     profile_form = PlayerProfileForm(instance=request.user.player)
        #     print("player is not None")

        # scout = getattr(request.user, 'scout', None)
        # if scout is not None:
        #     print("scout is not None")
        #     profile_form = ScoutProfileForm(instance=request.user.scout)

        # coach = getattr(request.user, 'coach', None)
        # if coach is not None:
        #     print("coach is not None")
        #     profile_form = CoachProfileForm(instance=request.user.coach)

        # # args.update(csrf(request))
        # args['form'] = form
        # args['profile_form'] = profile_form
        
        return render(request, 'theme/edit_account_player.html', args)


@login_required
def edit_account_scout(request):
    if request.method == 'POST':
        print('request.method == post')
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = ScoutProfileForm(request.POST, instance=request.user.scout)  # request.FILES is show the selected image or file

        print("request.FILES")
        print("request.FILES")
        print("request.FILES")
        # print(request.POST)
        print(request.FILES)
        if form.is_valid() and profile_form.is_valid():
            print("form.is_valid")

            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            # return redirect('player_list')
            success = True

            return render(request, 'theme/edit_account_scout.html', {'form': form, 'profile_form': profile_form, 'success': success})

        else:
            print('Error kut')
            print(form.errors)

            print('profile_form kut')
            print(profile_form.errors)
            # form = EditProfileForm(instance=request.user)
            # profile_form = PlayerProfileForm(instance=request.user.player)

            return render(request, 'theme/edit_account_scout.html', {'form': form, 'profile_form': profile_form})

            # return render(request, 'your_template.html', {'form': form, 'profile_form': profile_form})

    else:
        args = {}

        # form = EditProfileForm(instance=request.user)
        # # form = EditUserForm69(instance=request.user)

        # player = getattr(request.user, 'player', None)
        # if player is not None:
        #     profile_form = PlayerProfileForm(instance=request.user.player)
        #     print("player is not None")

        # scout = getattr(request.user, 'scout', None)
        # if scout is not None:
        #     print("scout is not None")
        #     profile_form = ScoutProfileForm(instance=request.user.scout)

        # coach = getattr(request.user, 'coach', None)
        # if coach is not None:
        #     print("coach is not None")
        #     profile_form = CoachProfileForm(instance=request.user.coach)

        # # args.update(csrf(request))
        # args['form'] = form
        # args['profile_form'] = profile_form
        
        return render(request, 'theme/edit_account_scout.html', args)



@login_required
def edit_account_agent(request):
    if request.method == 'POST':
        print('request.method == post')
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = AgentProfileForm(request.POST, instance=request.user.agent)  # request.FILES is show the selected image or file

        print("request.FILES")
        # print(request.POST)
        print(request.FILES)
        if form.is_valid() and profile_form.is_valid():
            print("form.is_valid")

            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            # return redirect('player_list')
            success = True

            return render(request, 'theme/edit_account_agent.html', {'form': form, 'profile_form': profile_form, 'success': success})

        else:
            print('Error kut')
            print(form.errors)

            print('profile_form kut')
            print(profile_form.errors)
            # form = EditProfileForm(instance=request.user)
            # profile_form = PlayerProfileForm(instance=request.user.player)

            return render(request, 'theme/edit_account_agent.html', {'form': form, 'profile_form': profile_form})

            # return render(request, 'your_template.html', {'form': form, 'profile_form': profile_form})

    else:
        args = {}

        # form = EditProfileForm(instance=request.user)
        # # form = EditUserForm69(instance=request.user)

        # player = getattr(request.user, 'player', None)
        # if player is not None:
        #     profile_form = PlayerProfileForm(instance=request.user.player)
        #     print("player is not None")

        # scout = getattr(request.user, 'scout', None)
        # if scout is not None:
        #     print("scout is not None")
        #     profile_form = ScoutProfileForm(instance=request.user.scout)

        # coach = getattr(request.user, 'coach', None)
        # if coach is not None:
        #     print("coach is not None")
        #     profile_form = CoachProfileForm(instance=request.user.coach)

        # # args.update(csrf(request))
        # args['form'] = form
        # args['profile_form'] = profile_form
        
        return render(request, 'theme/edit_account_agent.html', args)

@login_required
def profile_experience(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections

    return render(request, 'theme/profile/profile_experience.html', args)



@login_required
def agent_profile_experience(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections

    return render(request, 'theme/profile/agent_profile/agent_profile_experience.html', args)

@login_required
def scout_profile_experience(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections

    return render(request, 'theme/profile/scout_profile/scout_profile_experience.html', args)



@login_required
def profile_connections(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps


    args['num_connections'] = user.num_connections()


    args['connected_users'] = user.connected_users()




    return render(request, 'theme/profile/profile_connections.html', args)


@login_required
def agent_profile_connections(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps


    args['num_connections'] = user.num_connections()


    args['connected_users'] = user.connected_users()

    return render(request, 'theme/profile/agent_profile/agent_profile_connections.html', args)

@login_required
def scout_profile_connections(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps


    args['num_connections'] = user.num_connections()


    args['connected_users'] = user.connected_users()

    return render(request, 'theme/profile/scout_profile/scout_profile_connections.html', args)


@login_required
def profile_statistics(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections

    return render(request, 'theme/profile/profile_statistics.html', args)


from .models import User, Media

@login_required
def profile_media(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections


    #     # Retrieve all media associated with the user
    # user_media = user.media_collection.all()

    # # Separate media into images and videos
    # user_images = [media for media in user_media if media.is_image()]
    # user_videos = [media for media in user_media if media.is_video()]
    # # all_user_videos = [media for media in user_media]

    # args['user_images'] = user_images
    # args['user_videos'] = user_videos
    # args['all_user_media'] = user_media


        # Retrieve all media associated with the user
    user_media = Media.objects.filter(post__user=user).exclude(file__exact='')
    args['user_media'] = user_media



    return render(request, 'theme/profile/profile_media.html', args)

@login_required
def agent_profile_media(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections


    #     # Retrieve all media associated with the user
    # user_media = user.media_collection.all()

    # # Separate media into images and videos
    # user_images = [media for media in user_media if media.is_image()]
    # user_videos = [media for media in user_media if media.is_video()]
    # # all_user_videos = [media for media in user_media]

    # args['user_images'] = user_images
    # args['user_videos'] = user_videos
    # args['all_user_media'] = user_media


        # Retrieve all media associated with the user
    user_media = Media.objects.filter(post__user=user).exclude(file__exact='')
    args['user_media'] = user_media



    return render(request, 'theme/profile/agent_profile/agent_profile_media.html', args)


@login_required
def scout_profile_media(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    exps = Experience.objects.filter(user=user).order_by('-to_date')
    args['exps'] = exps

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections


    #     # Retrieve all media associated with the user
    # user_media = user.media_collection.all()

    # # Separate media into images and videos
    # user_images = [media for media in user_media if media.is_image()]
    # user_videos = [media for media in user_media if media.is_video()]
    # # all_user_videos = [media for media in user_media]

    # args['user_images'] = user_images
    # args['user_videos'] = user_videos
    # args['all_user_media'] = user_media


        # Retrieve all media associated with the user
    user_media = Media.objects.filter(post__user=user).exclude(file__exact='')
    args['user_media'] = user_media



    return render(request, 'theme/profile/scout_profile/scout_profile_media.html', args)


@login_required
def profile(request, username):
    args = {}
    user = User.objects.get(username=username)
    args['user'] = user

    connections = Connection.objects.filter(Q(sender=user, accepted=True) | Q(receiver=user, accepted=True))
    num_connections = connections.count()
    args['num_connections'] = num_connections

    posts = Post.objects.filter(user=user)
    exps = Experience.objects.filter(user=user).order_by('-to_date')

    posts_with_duration = []
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)


    for post in posts:
        # Calculate the duration since the post was created
        duration = timesince(post.created_at)
        posts_with_duration.append((post, duration))

    posts_with_comments = []
    for post, duration in posts_with_duration:
        # Fetch comments for the current post
        comments = Comment.objects.filter(post=post)
        posts_with_comments.append((post, duration, comments))

    args['posts'] = posts_with_comments
    args['liked_posts'] = liked_posts
    args['exps'] = exps
    



    # Omarios: if req.post: post social media from profile page

    connection_request_sent = Connection.objects.filter(sender=request.user, receiver=user, accepted=False).exists()
    connection_request_received = Connection.objects.filter(sender=user, receiver=request.user, accepted=False).exists()
    connection_request_accepted = Connection.objects.filter(
            Q(sender=user, receiver=request.user, accepted=True) |
            Q(sender=request.user, receiver=user, accepted=True)
        ).exists()


    args['connection_request_sent'] = connection_request_sent
    args['connection_request_received'] = connection_request_received
    args['connection_request_accepted'] = connection_request_accepted
    
    print('connection_request_accepted')
    print(connection_request_accepted)
    print(connection_request_accepted)

    if connection_request_received:
        connection_request_received_id = Connection.objects.filter(sender=user, receiver=request.user).first().id
        args['connection_request_received_id'] = connection_request_received_id

    if connection_request_sent:
        connection_request_sent_id = Connection.objects.filter(sender=request.user, receiver=user).first().id
        
        zxc = Connection.objects.filter(sender=request.user, receiver=user)
        print(zxc)
        args['connection_request_sent_id'] = connection_request_sent_id


    if connection_request_accepted:
        connection_request_accepted_id = Connection.objects.filter(
            Q(sender=user, receiver=request.user, accepted=True) |
            Q(sender=request.user, receiver=user, accepted=True)
        ).first().id
        args['connection_request_accepted_id'] = connection_request_accepted_id


    if hasattr(user, 'scout') and user.scout:

        return render(request, 'theme/profile/scout_profile/scout_profile.html', args)
    elif hasattr(user, 'agent') and user.agent:
        return render(request, 'theme/profile/agent_profile/agent_profile.html', args)
    else:
        return render(request, 'theme/profile/profile.html', args)




@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        request.user.following.add(user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.following.remove(user_to_unfollow)
    return redirect('profile', username=username)





from .models import Like, Comment

from django.http import JsonResponse

def like_post(request, post_id):
    if request.method == 'POST':

        # Remove variable is used by JQuery to set style and text based on action (like, unlike)
        remove = False
        if not Like.objects.filter(user=request.user, post_id=post_id).exists():
            Like.objects.create(user=request.user, post_id=post_id)
        else:
            existing_like = Like.objects.filter(user=request.user, post_id=post_id).first()
            existing_like.delete()
            remove = True


        # Calculate the updated like count
        likes_count = Like.objects.filter(post_id=post_id).count()

        # Return the updated like count as JSON response
        return JsonResponse({'likes_count': likes_count, 'remove': remove})



def comment_post(request, post_id, text):
    if request.method == 'POST':

        comment = Comment.objects.create(user=request.user, post_id=post_id, text=text)

        # Calculate the updated like count
        comments_count = Comment.objects.filter(post_id=post_id).count()

        # Return the newly added comment data as JSON response
        response_data = {
            'first_name': comment.user.first_name,
            'last_name': comment.user.last_name,
            'text': comment.text,
            'imgurl' : comment.user.getProfileimageUrl,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the timestamp as needed
        }
        # Return the updated like count as JSON response
        return JsonResponse({'comments_count': comments_count, 'comment':response_data})


from .forms import ExperienceForm
from .models import Experience

def create_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            experience = form.save()
            # return redirect('profile', username=request.user.username)

            return JsonResponse({'success': True, 'message': 'Experience created successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

    # form = ExperienceForm()
    # return render(request, 'create_experience.html', {'form': form})


def create_player_stats(request):
    if request.method == 'POST':
        form = PlayerStatsForm(request.POST)
        if form.is_valid():
            print('suck')
            player_instance = form.save(commit=False)
            player_instance.user = request.user
            player_instance.save()
            print(player_instance)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)


def create_player_goals(request):
    if request.method == 'POST':
        form = PlayerGoalForm(request.POST)
        if form.is_valid():
            goals_number = form.cleaned_data['goals']
            player_instance = get_object_or_404(Player, user=request.user)
            player_instance.goals = goals_number
            player_instance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)



def create_player_assists(request):
    if request.method == 'POST':
        form = PlayerAssistForm(request.POST)
        if form.is_valid():
            assists = form.cleaned_data['assists']
            player_instance = get_object_or_404(Player, user=request.user)
            player_instance.assists = assists
            player_instance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)





def create_player_cleansheet(request):
    if request.method == 'POST':
        form = PlayerCleanSheetForm(request.POST)
        if form.is_valid():
            clean_sheet = form.cleaned_data['clean_sheet']
            player_instance = get_object_or_404(Player, user=request.user)
            player_instance.clean_sheet = clean_sheet
            player_instance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)





def create_player_playedmatches(request):
    if request.method == 'POST':
        form = PlayerPlayedMatchesForm(request.POST)
        if form.is_valid():
            print('suck')
            player_instance = form.save(commit=False)
            player_instance.user = request.user
            player_instance.save()
            print(player_instance)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)




from django.db.models import Q
from datetime import date

def discover(request):

    # Get distinct positions and locations from the database
    distinct_positions = Player.objects.order_by('position').values_list('position', flat=True).distinct()
    distinct_locations = User.objects.order_by('place').values_list('place', flat=True).distinct()
    # Exclude 'None' values from distinct_positions and distinct_locations
    distinct_positions = [pos for pos in distinct_positions if pos is not None]
    distinct_locations = [loc for loc in distinct_locations if loc is not None]

    if request.method == 'POST':
        searched = request.POST.get('searched')
        position = request.POST.get('position')
        age = request.POST.get('age')
        location = request.POST.get('location')

        print(searched)
        print(position)
        print(age)
        print(location)

        users = User.objects.filter(
            Q(first_name__icontains=searched) |
            Q(last_name__icontains=searched) |
            Q(email__icontains=searched) |
            Q(place__icontains=searched) |
            Q(country__icontains=searched)
        )

        # Filter by player position
        if position is not None:
            users = users.filter(player__position__icontains=position)

        # Filter by age
        if age is not None:
            today = date.today()
            birth_year = today.year - int(age)
            users = users.filter(date_of_birth__year=birth_year)

        # Filter by location
        if location is not None:
            users = users.filter(place__icontains=location)

        return render(request, 'theme/discover.html', {'users': users, 'searched': searched, 'position': position, 'age': age, 'location': location, 'distinct_positions': distinct_positions, 'distinct_locations': distinct_locations})
    else:
        users = User.objects.all()

        return render(request, 'theme/discover.html', {'users': users, 'distinct_positions': distinct_positions, 'distinct_locations': distinct_locations})


from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')


from .models import Connection
from django.contrib import messages

def send_connection(request, username):
    if request.method == 'POST':
        receiver = get_object_or_404(User, username=username)

        # Check if a connection already exists
        existing_connection = Connection.objects.filter(sender=request.user, receiver=receiver).first()

        if existing_connection:
            return JsonResponse({'success': False, 'message': 'Connection already exists'})
        else:
            # Create a new connection
            connection = Connection.objects.create(sender=request.user, receiver=receiver)
            return JsonResponse({'success': True, 'message': 'Connection request sent'})

    # Handle other HTTP methods if needed
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Connection

def accept_connection(request, connection_id):
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user, accepted=False)
    connection.accepted = True
    connection.save()
    return JsonResponse({'success': True})

def delete_connection(request, connection_id):
    # connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    print(connection_id)
    print(connection_id)
    

    
    connection1 = Connection.objects.filter(id=connection_id, sender=request.user).first()
    print('connection1')
    print(connection1)
    
    connection2 = Connection.objects.filter(id=connection_id, receiver=request.user).first()

    print('connection2')
    print(connection2)

    if connection1:
        print('if connection1:')
        connection1.delete()
    else:
        print('else')
        connection2.delete()





    # connection = Connection.objects.filter(id=connection_id, receiver=request.user).first()
    # connection.delete()

    return JsonResponse({'success': True})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db import models

@login_required
def chat(request, user_username):
    receiver = get_object_or_404(User, username=user_username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
    # if request.method == 'GET':
    #     return JsonResponse({'messages': messages})

    return render(request, 'chat/chat.html', {'receiver': receiver, 'messages': messages})


@login_required
def chat2(request, user_username):
    receiver = get_object_or_404(User, username=user_username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
    # if request.method == 'GET':
    #     return JsonResponse({'messages': messages})

    return render(request, 'chat/chat2.html', {'receiver': receiver, 'messages': messages})


@login_required
def vacancies(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies})

@login_required
def create_vacancy(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.agent = request.user.agent
            vacancy.save()
            return redirect('vacancies')
    else:
        form = VacancyForm()

    return render(request, 'vacancies/create_vacancy.html', {'form': form})

from .forms import ApplicationForm

def vacancy_detail(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    related_vacancies = Vacancy.objects.all().exclude(id=vacancy.id)[:3]
    applications = vacancy.applications.all()

    if request.method == 'POST':
        player = request.user.player

        form = ApplicationForm(request.POST)
        if form.is_valid():
            motivation = form.cleaned_data['motivation']
            Application.objects.create(vacancy=vacancy, player=player, motivation=motivation)
            vacancy.save()

    else:
        form = ApplicationForm()

    return render(request, 'vacancies/vacancy_detail.html', {'vacancy': vacancy, 'related_vacancies':related_vacancies, 'form':form, 'applications': applications})



