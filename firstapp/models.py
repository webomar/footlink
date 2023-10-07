from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    is_player = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_scout = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images', default='/static/profile.jpg', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images', blank=True, null=True)
    place = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)

    def getImageUrl(self):
        if not self.profile_image:
            # depending on your template
            return '/static/profile.jpg'
        else:
        # Return the URL of the uploaded image
            return self.profile_image.url


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
    club = models.CharField(max_length=255, null=True)
    nft = models.CharField(max_length=255, null=True)
    competition = models.CharField(max_length=255, null=True)
    length = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    preferred_leg = models.CharField(max_length=10, null=True)
    position = models.CharField(max_length=255, null=True)
    qualities = models.CharField(max_length=255, null=True)
    career_statistics = models.CharField(max_length=255, null=True)
    ambition = models.TextField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    media_collection = models.ManyToManyField('Post', related_name='players', blank=True)
    followed_players = models.ManyToManyField(User, related_name='followed')    
    posts = models.ManyToManyField('Post', related_name='player_posts', blank=True)

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

    followed_players = models.ManyToManyField(User, related_name='scouts')
    player_notes = models.TextField()
    posts = models.ManyToManyField('Post', related_name='scout_posts')
    
    def __str__(self):
        return self.user.email

# Zaakwaarnemer model
class Zaakwaarnemer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='zaakwaarnemer')




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
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # This field will automatically set the current date and time when a post is created
    likes = models.ManyToManyField(User, related_name='liked_posts', through=Like, null=True, blank=True)
    comments = models.ManyToManyField(User, related_name='post_comments', through=Comment, null=True, blank=True)

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
    file = models.FileField(upload_to='post_media')
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




class Posttest(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
