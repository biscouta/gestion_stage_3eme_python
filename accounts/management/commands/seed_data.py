from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Profile
from applications.models import Application
from internships.models import InternshipOffer


class Command(BaseCommand):
    help = "Create fake demo data for the internship management project."

    def handle(self, *args, **options):
        password = "test12345"
        today = timezone.localdate()

        students_data = [
            {
                "username": "student_test",
                "email": "student@test.com",
                "full_name": "Etudiant Test",
                "phone": "0600000001",
                "field": "Developpement informatique",
                "study_level": "Bac+2",
                "skills": "Python, Django, HTML, CSS, Bootstrap, SQL",
            },
            {
                "username": "amina_dev",
                "email": "amina@test.com",
                "full_name": "Amina El Mourabit",
                "phone": "0612457890",
                "field": "Genie logiciel",
                "study_level": "Bac+3",
                "skills": "Django, React, JavaScript, Git",
            },
            {
                "username": "youssef_data",
                "email": "youssef@test.com",
                "full_name": "Youssef Benali",
                "phone": "0661122334",
                "field": "Data science",
                "study_level": "Bac+4",
                "skills": "Python, SQL, Power BI, Analyse de donnees",
            },
            {
                "username": "salma_ui",
                "email": "salma@test.com",
                "full_name": "Salma Idrissi",
                "phone": "0677788990",
                "field": "Design digital",
                "study_level": "Bac+2",
                "skills": "HTML, CSS, Bootstrap, Figma, UX/UI",
            },
        ]

        companies_data = [
            {
                "username": "company_test",
                "email": "company@test.com",
                "company_name": "Tech School SARL",
                "phone": "0600000002",
                "sector": "Informatique",
                "address": "Casablanca",
                "description": "Entreprise specialisee dans les solutions web et les plateformes educatives.",
            },
            {
                "username": "digital_factory",
                "email": "contact@digitalfactory.test",
                "company_name": "Digital Factory",
                "phone": "0522001122",
                "sector": "Developpement web",
                "address": "Rabat",
                "description": "Agence digitale qui accompagne les entreprises dans leur transformation numerique.",
            },
            {
                "username": "data_plus",
                "email": "rh@dataplus.test",
                "company_name": "Data Plus",
                "phone": "0524556677",
                "sector": "Business intelligence",
                "address": "Marrakech",
                "description": "Cabinet specialise dans la data, les tableaux de bord et l'aide a la decision.",
            },
        ]

        students = [self.create_student(data, password) for data in students_data]
        companies = [self.create_company(data, password) for data in companies_data]

        offers_data = [
            {
                "company": companies[0],
                "title": "Stage developpeur Django",
                "description": "Participation au developpement d'une application web avec Django et Bootstrap.",
                "domain": "Web",
                "required_skills": "Python, Django, HTML, CSS, Bootstrap",
                "duration": "2 mois",
                "location": "Casablanca",
                "internship_type": "hybride",
                "deadline": today + timedelta(days=30),
                "status": "open",
            },
            {
                "company": companies[0],
                "title": "Stage maintenance application web",
                "description": "Correction de bugs, amelioration de pages et tests fonctionnels.",
                "domain": "Maintenance",
                "required_skills": "Django, Git, Debugging",
                "duration": "3 mois",
                "location": "Casablanca",
                "internship_type": "presentiel",
                "deadline": today + timedelta(days=12),
                "status": "closed",
            },
            {
                "company": companies[1],
                "title": "Stage frontend Bootstrap",
                "description": "Creation d'interfaces modernes, simples et responsives avec Bootstrap 5.",
                "domain": "Frontend",
                "required_skills": "HTML, CSS, Bootstrap, JavaScript",
                "duration": "1 mois",
                "location": "Rabat",
                "internship_type": "remote",
                "deadline": today + timedelta(days=20),
                "status": "open",
            },
            {
                "company": companies[1],
                "title": "Stage UI UX designer",
                "description": "Preparation de maquettes, amelioration de parcours utilisateurs et prototypes.",
                "domain": "Design",
                "required_skills": "Figma, UX/UI, HTML, CSS",
                "duration": "2 mois",
                "location": "Rabat",
                "internship_type": "hybride",
                "deadline": today + timedelta(days=25),
                "status": "open",
            },
            {
                "company": companies[2],
                "title": "Stage base de donnees SQLite",
                "description": "Conception de tables, requetes SQL et preparation de rapports simples.",
                "domain": "Base de donnees",
                "required_skills": "SQL, SQLite, Modelisation",
                "duration": "6 semaines",
                "location": "Marrakech",
                "internship_type": "presentiel",
                "deadline": today + timedelta(days=15),
                "status": "open",
            },
            {
                "company": companies[2],
                "title": "Stage analyse de donnees",
                "description": "Nettoyage de donnees, creation de tableaux de bord et analyse descriptive.",
                "domain": "Data",
                "required_skills": "Python, SQL, Excel, Power BI",
                "duration": "3 mois",
                "location": "Marrakech",
                "internship_type": "remote",
                "deadline": today + timedelta(days=35),
                "status": "open",
            },
        ]

        offers = []
        for offer_data in offers_data:
            company = offer_data.pop("company")
            offer, _created = InternshipOffer.objects.update_or_create(
                company=company,
                title=offer_data["title"],
                defaults=offer_data,
            )
            offers.append(offer)

        applications_data = [
            (students[0], offers[0], "Je souhaite travailler sur une application Django complete.", "pending"),
            (students[0], offers[2], "Je suis interesse par le frontend et Bootstrap.", "accepted"),
            (students[1], offers[0], "Mon profil correspond bien aux technologies demandees.", "accepted"),
            (students[1], offers[3], "Je peux contribuer aux interfaces et aux tests utilisateurs.", "pending"),
            (students[2], offers[4], "Je suis motive par la modelisation et les bases SQL.", "rejected"),
            (students[2], offers[5], "Je souhaite approfondir mes competences en data.", "pending"),
            (students[3], offers[2], "Je veux ameliorer mes competences frontend.", "pending"),
            (students[3], offers[3], "Cette offre UI UX correspond parfaitement a mon profil.", "accepted"),
        ]

        for student, offer, message, status in applications_data:
            Application.objects.update_or_create(
                student=student,
                offer=offer,
                defaults={
                    "message": message,
                    "status": status,
                },
            )

        self.stdout.write(self.style.SUCCESS("Fake data ajoutees avec succes."))
        self.stdout.write("Mot de passe pour tous les comptes : test12345")
        self.stdout.write("Comptes etudiants : student_test, amina_dev, youssef_data, salma_ui")
        self.stdout.write("Comptes entreprises : company_test, digital_factory, data_plus")

    def create_student(self, data, password):
        user = self.create_user(data["username"], data["email"], password)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                "role": "student",
                "full_name": data["full_name"],
                "phone": data["phone"],
                "field": data["field"],
                "study_level": data["study_level"],
                "skills": data["skills"],
            },
        )
        return user

    def create_company(self, data, password):
        user = self.create_user(data["username"], data["email"], password)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                "role": "company",
                "full_name": data["company_name"],
                "company_name": data["company_name"],
                "phone": data["phone"],
                "sector": data["sector"],
                "address": data["address"],
                "description": data["description"],
            },
        )
        return user

    def create_user(self, username, email, password):
        user, _created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.set_password(password)
        user.save()
        return user
