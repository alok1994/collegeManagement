from django import forms
from .models import Fee
from fee_structure.models import Semester

class FeeForm(forms.ModelForm):  # Change from forms.Form to forms.ModelForm
    class Meta:
        model = Fee
        exclude = ['student', 'receipt_number', 'total_amount_in_words', 'fee_for_month', 'semester' , 'comments']