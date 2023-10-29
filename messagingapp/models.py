# messagingapp/models.py
from django.db import models

class Message(models.Model):
    semester = models.CharField(max_length=20)
    message_text = models.TextField()

    def __str__(self):
        return self.semester
