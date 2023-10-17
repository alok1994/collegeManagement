from django.db import models
#from admissionapp.models import AdmissionForm

class CharacterCertificate(models.Model):
    student = models.ForeignKey('admissionapp.AdmissionForm', on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    # You can add more fields specific to the character certificate here.

    def __str__(self):
        return f"Character Certificate for {self.student.first_name} {self.student.last_name}"
