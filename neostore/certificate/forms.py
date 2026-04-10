from django import forms
from django.forms import ModelForm, TextInput, FileInput
from home.models import Certificate


class CertificateForm(ModelForm):
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
            if photo.content_type not in allowed_types:
                raise forms.ValidationError('Разрешены только изображения (JPG, PNG, GIF) и PDF файлы.')
        return photo

    class Meta:
        model = Certificate
        fields = ['name', 'givenfor', 'photo']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'givenfor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Выдана за'}),
            'photo': FileInput(attrs={'class': 'form-control', 'placeholder': 'Файл', 'accept': '.pdf,.jpg,.jpeg,.png,.gif'}),
        }
