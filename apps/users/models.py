from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure unique emails
    profile_picture = models.ImageField(
         upload_to='profile_pics/', 
         null=True, 
         blank=True, 
         default='profile_pics/default.png'  # Set a default image
     )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username