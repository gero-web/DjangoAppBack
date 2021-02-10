from django.db import models

# Create your models here.

class Task(models.Model):
        
       name = models.CharField(max_length=255)
       desctiption = models.CharField(max_length=255)

       class Meta:
        permissions = [
            ("add", "Can add"),
            ("change", "Can put"),
            ("delete", "Can remove "),
              ("a", "add"),
            ("c", "change"),
            ("d", "delete"),
        ]


