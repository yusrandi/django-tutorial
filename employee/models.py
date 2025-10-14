from django.db import models

# Create your models here.


# langkah kedua tambahkn field dgn type FileField
class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to="profile/", null=True, blank=True)

    def __str__(self):
        return self.name
