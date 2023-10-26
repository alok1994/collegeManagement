from django.db import models

class Semester(models.Model):
    semester_number = models.PositiveIntegerField(unique=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2)
    sport_fee = models.DecimalField(max_digits=10, decimal_places=2)
    miscellaneous_fee = models.DecimalField(max_digits=10, decimal_places=2)
    semester_total =  models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Semester {self.semester_number}'
