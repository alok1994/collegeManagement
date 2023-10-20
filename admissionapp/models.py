from django.db import models

class AdmissionForm(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True,)
    last_name = models.CharField(max_length=50, blank=True,)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='admission_photos/')
    marks_10th = models.DecimalField(max_digits=5, decimal_places=2)
    marks_12th = models.DecimalField(max_digits=5, decimal_places=2)
    admission_batch = models.CharField(max_length=20)
    school_details_12th = models.TextField()
    school_details_10th = models.TextField()
    address = models.TextField()
    pass_out_year_12th = models.IntegerField()
    pass_out_year_10th = models.IntegerField()
    admission_date = models.DateField()
    caste = models.CharField(max_length=20)
    roll_number_12th = models.CharField(max_length=20)
    roll_number_10th = models.CharField(max_length=20)
    aadhar_number = models.CharField(max_length=12, unique=True)
    mobile_number = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    subjects = models.CharField(max_length=1000) 
    registration_number = models.CharField(max_length=20, blank=True,)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
