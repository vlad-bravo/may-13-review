from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('company_name', 'phone', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Этот аккаунт неактивен.",
                code='inactive',
            )


class TelegramConnectForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        min_length=6,
        label='Код подтверждения',
        help_text='Введите 6-значный код, который вы отправили боту'
    )
