from django.forms import ModelForm, TextInput, FileInput
from home.models import Certificate


class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'givenfor', 'photo']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'givenfor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Given for '}),
            'photo': FileInput(attrs={'class': 'form-control', 'placeholder': 'Photo', 'accept': 'image/*'}),
        }
