from django.contrib.auth.models import User
from django.db import models

from internships.models import InternshipOffer


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptee'),
        ('rejected', 'Rejetee'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(InternshipOffer, on_delete=models.CASCADE)
    message = models.TextField()
    cv = models.FileField(upload_to='applications_cv/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'offer'],
                name='unique_student_offer_application',
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.offer.title}"
