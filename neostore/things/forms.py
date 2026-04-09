from home.models import Thing
from django.forms import ModelForm, TextInput, FileInput


class ThingsForm(ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'value', 'amount', 'photo']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'photo': FileInput(attrs={'class': 'form-control', 'placeholder': 'Фото', 'accept': 'image/*'}),
            'value': TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'amount': TextInput(attrs={'class': 'form-control', 'placeholder': 'Количество'}),
        }
