from django import forms
from .models import CharacterCertificate

class CharacterCertificateForm(forms.ModelForm):
    class Meta:
        model = CharacterCertificate
        fields = '__all__'
