from django import forms
from .models import AdmissionForm

class AdmissionFormForm(forms.ModelForm):
    class Meta:
        model = AdmissionForm
        fields = '__all__'

    photo = forms.ImageField(required=False)

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionForm
        fields = '__all__'  # Use all fields from the Admission model

AdmissionFormForm.base_fields['photo'].widget.attrs.update({'enctype': 'multipart/form-data'})