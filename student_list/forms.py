from django import forms
from admissionapp.models import AdmissionForm

class AdmissionFormForm(forms.ModelForm):  # Renamed the form class
    class Meta:
        model = AdmissionForm
        fields = '__all__'

class AdmissionYearFilterForm(forms.Form):
    admission_year = forms.IntegerField(label='Year of Admission', required=False)

class AdmissionClassFilterForm(forms.Form):
    admission_batch = forms.CharField(label='Admission Batch', required=False)

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionForm
        fields = '__all__'  # Use all fields from the Admission model

# Ensure enctype attribute is set for file uploads
StudentUpdateForm.base_fields['photo'].widget.attrs.update({'enctype': 'multipart/form-data'})
