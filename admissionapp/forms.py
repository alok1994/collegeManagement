from django import forms
from .models import AdmissionForm

class AdmissionFormForm(forms.ModelForm):
    class Meta:
        model = AdmissionForm
        fields = '__all__'
