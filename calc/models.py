from django.db import models

# Create your models here.
class Contact (models.Model):
    first_name = models.CharField(max_length=30, null=True,
   blank=True)
    last_name = models.CharField(max_length=30, null=True,
   blank=True)
    email = models.EmailField(null=True,
   blank=True)
    comment = models.TextField(null=True,
   blank=True)
    date=models.DateField()
    
    def __str__(self):
        return self.first_name

    