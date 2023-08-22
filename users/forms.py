from django.contrib.auth.forms import UserCreationForm

from users.models import UserABC


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserABC
        fields = UserCreationForm.Meta.fields + ("email",)
