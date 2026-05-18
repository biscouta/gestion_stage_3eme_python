from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Etudiant'),
        ('company', 'Entreprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # infos etudiant
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    field = models.CharField(max_length=100, blank=True)
    study_level = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)

    # infos entreprise
    company_name = models.CharField(max_length=150, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.full_name
