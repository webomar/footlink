from .models import Coach, Player, Scout, Zaakwaarnemer, Post
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from django.contrib.auth import get_user_model

User = get_user_model()

@modeladmin_register
class PlayerAdmin(ModelAdmin):
    model = Player
    menu_icon = 'user'
    menu_label = 'Players'

@modeladmin_register
class PostAdmin(ModelAdmin):
    model = Post

@modeladmin_register
class CoachAdmin(ModelAdmin):
    model = Coach
    menu_icon = 'user'
    menu_label = 'Coaches'

@modeladmin_register
class ScoutAdmin(ModelAdmin):
    model = Scout
    menu_icon = 'user'
    menu_label = 'Scouts'
    # list_display = ('username',)
    # search_fields = ('username',)

@modeladmin_register
class ZaakwaarnemerAdmin(ModelAdmin):
    model = Zaakwaarnemer
    menu_icon = 'user'
    menu_label = 'Zaakwaarnemers'
    list_display = ('username',)
    search_fields = ('username',)

# Register the default User model with a custom label
@modeladmin_register
class UserAdmin(ModelAdmin):
    model = User
    menu_icon = 'user'
    menu_label = 'Users'

