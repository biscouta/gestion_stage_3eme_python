from django.contrib.auth.models import User
from django.db import models


class InternshipOffer(models.Model):
    TYPE_CHOICES = [
        ('presentiel', 'Presentiel'),
        ('remote', 'Remote'),
        ('hybride', 'Hybride'),
    ]

    STATUS_CHOICES = [
        ('open', 'Ouverte'),
        ('closed', 'Fermee'),
    ]

    company = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    domain = models.CharField(max_length=100)
    required_skills = models.TextField()
    duration = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    internship_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
