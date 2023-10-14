from django import forms
from .models import Fee

class FeeForm(forms.ModelForm):  # Change from forms.Form to forms.ModelForm
    class Meta:
        model = Fee
        fields = ['amount', 'payment_date', 'month']

