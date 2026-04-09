from django.forms import ModelForm, TextInput
from home.models import Certificate


class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'givenfor']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'givenfor': TextInput(attrs={'class': 'form-control', 'placeholder': 'За что'}),
        }
