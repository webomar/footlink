from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db.models import Q


class User(AbstractUser):
    is_player = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_scout = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='media/profile_images', blank=True, null=True)
    cover_image = models.ImageField(upload_to='media/cover_images', blank=True, null=True)
    place = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.IntegerField(null=True)
    # media_collection = models.ManyToManyField('Post', related_name='players', blank=True)
    followed_users = models.ManyToManyField('User', related_name='followed')    
    posts = models.ManyToManyField('Post', related_name='player_posts', blank=True)
    about = models.TextField(null=True, blank=True)

    def getFullName(self):
        return self.getFirstName()+" "+self.getLastName()
    
    def getFirstName(self):
        if self.first_name:
            return self.first_name
        else:
            return ''

    def getLastName(self):
        if self.last_name:
            return self.last_name
        else:
            return ''

    def getAbout(self):
        if not self.about:
            # depending on your template
            return 'Nothing to show here...'
        else:
        # Return the URL of the uploaded image
            return self.about

    def getProfileimageUrl(self):
        if not self.profile_image:
            # depending on your template
            return '/static/profile_placeholder.jpg'
        else:
        # Return the URL of the uploaded image
            return self.profile_image.url
        
    def getCoverimageUrl(self):
        if not self.cover_image:
            # depending on your template
            return '/static/cover_placeholder.jpg'
        else:
        # Return the URL of the uploaded image
            return self.cover_image.url
        
    def connections(self):
        sent_connections = self.connection_requests_sent.filter(accepted=True)
        received_connections = self.connection_requests_received.filter(accepted=True)
        return sent_connections | received_connections
    
    def connections_received_onhold(self):
        received_connections = self.connection_requests_received.filter(accepted=False)
        return received_connections

    # Get the people whom the user is connected with
    def connected_users(self):
        connections = self.connections()
        connected_users = []
        for connection in connections:
            if connection.sender == self:
                connected_users.append(connection.receiver)
            else:
                connected_users.append(connection.sender)
        return connected_users
    
    def is_connected(self, user_id):
        other_user = User.objects.get(id=user_id)
        connection_exists = Connection.objects.filter(
            (Q(sender=self) & Q(receiver=other_user)) | (Q(sender=other_user) & Q(receiver=self)),
            accepted=True
        ).exists()
        return connection_exists
    
    def num_connections(self):
        return self.connections().count()

    def getPosition(self):
        if self.player:
            return self.player.position
        
    def getClub(self):
        if self.player:
            return self.player.club
        
class Connection(models.Model):
    sender = models.ForeignKey(User, related_name='connection_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='connection_requests_received', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)





class Experience(models.Model):
    club = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    club_image = models.ImageField(upload_to='media/club_images', blank=True, null=True)

    def __str__(self):
        if self.club != None:
            return self.club
        else:
            return 'No Club'
        
    def getClubImageUrl(self):
        if not self.club_image:
            # depending on your template
            return '/static/profile_placeholder.jpg'

        else:
        # Return the URL of the uploaded image
            return self.club_image.url
        
    def get_to_date(self):
        if not self.to_date:
            return 'Present'
        else:
            return self.to_date

User.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through='UserFollowing',
        related_name='followers',
        symmetrical=False,
    )
)
class UserFollowing(models.Model):
    from_user = models.ForeignKey(
        User, related_name='following_set', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='followers_set', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)



class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='player')

    # Add additional fields specific to each user type
    club = models.CharField(max_length=255, null=True, blank=True)
    team = models.CharField(max_length=255, null=True, blank=True)
    nft = models.CharField(max_length=255, null=True, blank=True) # national football team
    competition = models.CharField(max_length=255, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True)
    preferred_leg = models.CharField(max_length=10, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    qualities = models.CharField(max_length=255, null=True, blank=True)
    career_statistics = models.CharField(max_length=255, null=True, blank=True)
    ambition = models.TextField(null=True, blank=True)
    goals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    clean_sheet = models.IntegerField(null=True, blank=True)
    played_matches = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.email




# Coach model
class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='coach')
    def __str__(self):
        return self.user.email

# Scout model
class Scout(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='scout')

    player_notes = models.TextField()
    posts = models.ManyToManyField('Post', related_name='scout_posts')
    
    def __str__(self):
        return self.user.email

# Scout model
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='agent')

    player_notes = models.TextField()
    posts = models.ManyToManyField('Post', related_name='agent_posts')
    
    def __str__(self):
        return self.user.email

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    place = models.CharField(max_length=255)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='posted_vacancies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Application(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    motivation = models.TextField()

    def __str__(self):
        return f"{self.player.username} - {self.vacancy.title}"



# Zaakwaarnemer model
class Zaakwaarnemer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='zaakwaarnemer')




from django.db import models

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', through=Like)
    comments = models.ManyToManyField(Comment, related_name='post_comments')

    # media = models.ManyToManyField(Media, related_name='posts', blank=True)

    def __str__(self):
        return f'Post #{self.pk}'

    def num_likes(self):
        return self.likes.count()

    def num_comments(self):
        return self.comments.count()

class Media(models.Model):
    MEDIA_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    media_type = models.CharField(max_length=5, choices=MEDIA_CHOICES)
    file = models.FileField(upload_to='media/post_media')
    # You can add more fields like captions, descriptions, etc., as needed.
    def is_image(self):
        # Check if the file extension indicates an image (you can add more image formats as needed)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        file_extension = self.file.name.lower()[-4:]
        return file_extension in image_extensions

    def is_video(self):
        # Check if the file extension indicates a video (you can add more video formats as needed)
        video_extensions = ['.mp4', '.avi', '.mov']
        file_extension = self.file.name.lower()[-4:]
        return file_extension in video_extensions
    def __str__(self):
        return f'{self.get_media_type_display()} #{self.pk}'


# models.py

from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
