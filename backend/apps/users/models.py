from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    INVESTOR_PROFILES = [
        ('CONSERVATIVE', 'Conservador'),
        ('MODERATE', 'Moderado'),
        ('AGGRESSIVE', 'Agressivo'),
    ]
    investor_profile = models.CharField(
        max_length=20, 
        choices=INVESTOR_PROFILES, 
        null=True, 
        blank=True
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
