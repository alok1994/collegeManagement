from django import forms
from .models import TransferCertificate

class CharacterCertificateForm(forms.ModelForm):
    class Meta:
        model = TransferCertificate
        fields = '__all__'
