# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser



# class UserCreateForm(UserCreationForm):
#     class Meta:
#         fields = ("email", "password1", "password2")
#         model = get_user_model()
#         db_table = "user_accounts"
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['email'].label = 'Display Name'  # labels for forms
#         self.fields['email'].label = 'Email Address'
#


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'mobile_number', 'password1', 'password2', 'is_handyman',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].label = "New Email Label"
        self.fields['is_handyman'].label = "I want to work as an Handyman"
        # self.fields['id email'].wid


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
