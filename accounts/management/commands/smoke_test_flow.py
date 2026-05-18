from datetime import timedelta
from uuid import uuid4

from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from applications.models import Application
from internships.models import InternshipOffer


class Command(BaseCommand):
    help = "Run a simple end-to-end demo flow with Django's test client."

    def handle(self, *args, **options):
        suffix = uuid4().hex[:8]
        company_username = f"company_flow_{suffix}"
        student_username = f"student_flow_{suffix}"
        password = "test12345"
        client = Client(HTTP_HOST="localhost")

        self.check_response(
            client.post(
                reverse("register_company"),
                {
                    "username": company_username,
                    "email": f"{company_username}@test.com",
                    "password": password,
                    "company_name": "Entreprise Flow Test",
                    "phone": "0611111111",
                    "sector": "Informatique",
                    "address": "Casablanca",
                    "description": "Compte entreprise pour test.",
                },
            ),
            "register company",
        )
        self.check_response(
            client.post(reverse("login"), {"username": company_username, "password": password}),
            "login company",
        )
        self.check_response(client.get(reverse("company_dashboard")), "company dashboard", expected=(200,))
        self.check_response(
            client.post(
                reverse("create_internship_company"),
                {
                    "title": "Offre scenario test",
                    "description": "Description de test pour une offre de stage.",
                    "domain": "Web",
                    "required_skills": "Django, Bootstrap, SQLite",
                    "duration": "2 mois",
                    "location": "Casablanca",
                    "internship_type": "hybride",
                    "deadline": (timezone.localdate() + timedelta(days=30)).isoformat(),
                    "status": "open",
                },
            ),
            "create offer",
        )
        offer = InternshipOffer.objects.get(company__username=company_username, title="Offre scenario test")
        self.check_response(client.get(reverse("company_internship_list")), "company offers", expected=(200,))
        self.check_response(client.get(reverse("logout")), "logout company")

        self.check_response(
            client.post(
                reverse("register_student"),
                {
                    "username": student_username,
                    "email": f"{student_username}@test.com",
                    "password": password,
                    "full_name": "Etudiant Flow Test",
                    "phone": "0622222222",
                    "field": "Informatique",
                    "study_level": "Bac+2",
                    "skills": "Django, HTML, CSS",
                },
            ),
            "register student",
        )
        self.check_response(
            client.post(reverse("login"), {"username": student_username, "password": password}),
            "login student",
        )
        self.check_response(client.get(reverse("student_internship_list")), "student offer list", expected=(200,))
        self.check_response(client.get(reverse("apply_for_internship", args=[offer.pk])), "apply page", expected=(200,))
        self.check_response(
            client.post(reverse("apply_for_internship", args=[offer.pk]), {"message": "Je souhaite postuler a cette offre."}),
            "post application",
        )
        self.check_response(client.get(reverse("student_applications")), "student applications", expected=(200,))
        application = Application.objects.get(student__username=student_username, offer=offer)
        self.check_response(client.get(reverse("logout")), "logout student")

        self.check_response(
            client.post(reverse("login"), {"username": company_username, "password": password}),
            "relogin company",
        )
        self.check_response(
            client.get(reverse("company_internship_applications", args=[offer.pk])),
            "company received applications",
            expected=(200,),
        )
        self.check_response(client.post(reverse("accept_application_company", args=[application.pk])), "accept application")
        application.refresh_from_db()
        if application.status != "accepted":
            raise AssertionError("Application was not accepted.")

        self.check_response(client.post(reverse("reject_application_company", args=[application.pk])), "reject application")
        application.refresh_from_db()
        if application.status != "rejected":
            raise AssertionError("Application was not rejected.")

        self.stdout.write(self.style.SUCCESS("Scenario de test termine avec succes."))

    def check_response(self, response, label, expected=(200, 302)):
        if response.status_code not in expected:
            raise AssertionError(f"{label}: status {response.status_code}, expected {expected}")
