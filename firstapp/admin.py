from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    pass

class MediaAdmin(admin.ModelAdmin):
    pass

class LikeAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)