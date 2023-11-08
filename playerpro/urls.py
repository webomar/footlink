from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from firstapp.views import  feed, home, landing

from firstapp import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),



    # path('player/registration/', player_registration, name='player_registration'),
    # path('accounts/profile/', player_profile, name='player_profile'),
    # path("scout/", views.scout_home, name="scout-home"),
    # path("coach/", views.coach_home, name="coach-home"),
    path('players-list/', views.player_list, name='player_list'),
    path('players/<int:player_pk>/', views.player_detail, name='player_detail'),

    path("signup/coach/", views.CoachSignUpView.as_view(), name="coach-signup"),
    path("signup/scout/", views.ScoutSignUpView.as_view(), name="scout-signup"),


    # path("player/", views.player_home, name="player-home"),
    # path("update/", views.player_profile, name="player-profile"),
    # path("edit/", views.edit_profile, name="edit_profile"),
    # path('old_home', home, name='home'),
    path('', landing, name='landing'),
    path('feed/', feed, name='feed'),
    path('feed_test/', views.feed_test, name='feed_test'),
    path("edit-account/", views.edit_account, name="edit_account"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/player/", views.PlayerSignUpView.as_view(), name="player-signup"),
    path('logout/', views.logout_view, name="logout"),
    path('discover/', views.discover, name="discover"),















    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('comment_post/<int:post_id>/<str:text>/', views.comment_post, name='comment_post'),




]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),




    # path('scout/registration/', scout_registration, name='scout_registration'),
    # path('zaakwaarnemer/registration/', zaakwaarnemer_registration, name='zaakwaarnemer_registration'),
    # path('coach/registration/', coach_registration, name='coach_registration'),

]
