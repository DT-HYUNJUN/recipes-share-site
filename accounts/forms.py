from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'email',
            'nickname',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'profile_image',
            'birthdate'
        )


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'nickname',
            'email',
            'first_name',
            'last_name',
            'profile_image',
            'birthdate'
        )


class CustomAuthenticationForm(AuthenticationForm):
    pass