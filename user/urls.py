from django.conf.urls import url
from user.views import ApiUser, ApiTheme, ApiUserCard
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^user/$', ApiUser.as_view()),
    url(r'^auth/$', views.obtain_auth_token),
    url(r'^theme/$', ApiTheme.as_view()),
    url(r'^user-card/$', ApiUserCard.as_view()),
]