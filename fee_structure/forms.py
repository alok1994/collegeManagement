from django import forms
from .models import Semester

class SemesterFeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['registration_fee','tuition_fee', 'exam_fee', 'sport_fee', 'miscellaneous_fee', 'semester_total']
