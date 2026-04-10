from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
        error_messages = {
            'username': {
                'required': 'Это поле обязательно.',
                'unique': 'Пользователь с таким именем уже существует.',
                'max_length': 'Имя пользователя слишком длинное.',
                'min_length': 'Имя пользователя должно содержать минимум 1 символ.',
            },
            'password2': {
                'required': 'Это поле обязательно.',
                'password_mismatch': 'Пароли не совпадают.',
            },
            'password1': {
                'required': 'Это поле обязательно.',
                'min_length': 'Пароль должен содержать минимум 8 символов.',
                'common': 'Пароль слишком простой.',
                'numeric': 'Пароль не может состоять только из цифр.',
            },
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'

    error_messages = {
        'invalid_login': 'Неверное имя пользователя или пароль.',
        'inactive': 'Этот аккаунт неактивен.',
    }