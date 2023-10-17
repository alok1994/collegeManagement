from django import forms
from .models import Fee

class FeeForm(forms.ModelForm):  # Change from forms.Form to forms.ModelForm
    class Meta:
        model = Fee
        exclude = ['student', 'receipt_number', 'total_amount_in_words']