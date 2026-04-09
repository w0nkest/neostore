from home.models import Thing
from django.forms import ModelForm, TextInput, FileInput


class ThingsForm(ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'value', 'amount', 'photo']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'photo': FileInput(attrs={'class': 'form-control', 'placeholder': 'Photo', 'accept': 'image/*'}),
            'value': TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'amount': TextInput(attrs={'class': 'form-control', 'placeholder': 'amount of things'}),
        }
