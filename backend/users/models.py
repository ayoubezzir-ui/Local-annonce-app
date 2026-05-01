from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from categories.models import Department

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('chef', 'Chef'),
        ('manager', 'Manager'),
        ('technicien', 'Technicien'),
        ('ingenieur', 'Ingénieur'),
        ('delegue', 'Délégué'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)