from django.urls import path

from users.views import profile_view, RegisterView

app_name = 'users'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('registration', RegisterView.as_view(), name='register'),
]
