from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from .models import Profile
from applications.models import Application
from internships.models import InternshipOffer


def redirect_by_role(user):
    profile = getattr(user, 'profile', None)

    if user.is_staff:
        return redirect('admin_dashboard')
    if profile and profile.role == 'student':
        return redirect('student_dashboard')
    if profile and profile.role == 'company':
        return redirect('company_dashboard')

    return redirect('login')


def get_user_role(user):
    profile = getattr(user, 'profile', None)
    return profile.role if profile else None


def require_admin(request):
    if not request.user.is_staff:
        messages.error(request, "Acces reserve a l'administration.")
        return redirect_by_role(request.user)
    return None


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        if not request.user.is_staff and not hasattr(request.user, 'profile'):
            logout(request)
            messages.error(request, "Votre compte n'a pas encore de profil.")
            return redirect('login')

        return redirect_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion reussie.")
            return redirect_by_role(user)

        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Deconnexion reussie.")
    return redirect('login')


@never_cache
def register_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe deja.")
            return redirect('register_student')

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(
            user=user,
            role='student',
            full_name=request.POST.get('full_name', ''),
            phone=request.POST.get('phone', ''),
            field=request.POST.get('field', ''),
            study_level=request.POST.get('study_level', ''),
            skills=request.POST.get('skills', ''),
            cv=request.FILES.get('cv'),
        )

        messages.success(request, "Compte etudiant cree avec succes.")
        return redirect('login')

    return render(request, 'accounts/register_student.html')


@never_cache
def register_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe deja.")
            return redirect('register_company')

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(
            user=user,
            role='company',
            full_name=company_name,
            company_name=company_name,
            phone=request.POST.get('phone', ''),
            sector=request.POST.get('sector', ''),
            address=request.POST.get('address', ''),
            description=request.POST.get('description', ''),
        )

        messages.success(request, "Compte entreprise cree avec succes.")
        return redirect('login')

    return render(request, 'accounts/register_company.html')


@login_required
def student_dashboard(request):
    if get_user_role(request.user) != 'student':
        messages.error(request, "Acces reserve aux etudiants.")
        return redirect_by_role(request.user)

    return render(request, 'accounts/student_dashboard.html')


@login_required
def company_dashboard(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Acces reserve aux entreprises.")
        return redirect_by_role(request.user)

    return render(request, 'accounts/company_dashboard.html')


@login_required
def student_profile(request):
    if get_user_role(request.user) != 'student':
        messages.error(request, "Acces reserve aux etudiants.")
        return redirect_by_role(request.user)

    return render(request, 'accounts/student_profile.html', {
        'profile': request.user.profile,
    })


@login_required
def company_profile(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Acces reserve aux entreprises.")
        return redirect_by_role(request.user)

    return render(request, 'accounts/company_profile.html', {
        'profile': request.user.profile,
    })


@login_required
@never_cache
def student_profile_edit(request):
    if get_user_role(request.user) != 'student':
        messages.error(request, "Acces reserve aux etudiants.")
        return redirect_by_role(request.user)

    profile = request.user.profile

    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', '')
        profile.phone = request.POST.get('phone', '')
        profile.field = request.POST.get('field', '')
        profile.study_level = request.POST.get('study_level', '')
        profile.skills = request.POST.get('skills', '')

        if request.FILES.get('cv'):
            profile.cv = request.FILES.get('cv')

        profile.save()
        messages.success(request, "Profil etudiant modifie avec succes.")
        return redirect('student_profile')

    return render(request, 'accounts/student_profile_edit.html', {
        'profile': profile,
    })


@login_required
@never_cache
def company_profile_edit(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Acces reserve aux entreprises.")
        return redirect_by_role(request.user)

    profile = request.user.profile

    if request.method == 'POST':
        profile.company_name = request.POST.get('company_name', '')
        profile.full_name = profile.company_name
        profile.phone = request.POST.get('phone', '')
        profile.sector = request.POST.get('sector', '')
        profile.address = request.POST.get('address', '')
        profile.description = request.POST.get('description', '')
        profile.save()

        messages.success(request, "Profil entreprise modifie avec succes.")
        return redirect('company_profile')

    return render(request, 'accounts/company_profile_edit.html', {
        'profile': profile,
    })


def register_supervisor(request):
    return redirect('register_company')


@login_required
def supervisor_dashboard(request):
    return redirect('company_dashboard')


@login_required
def supervisor_profile(request):
    return redirect('company_profile')


@login_required
def supervisor_profile_edit(request):
    return redirect('company_profile_edit')


@login_required
def admin_dashboard(request):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    return render(request, 'accounts/admin_dashboard.html', {
        'users_count': User.objects.count(),
        'profiles_count': Profile.objects.count(),
        'offers_count': InternshipOffer.objects.count(),
        'applications_count': Application.objects.count(),
    })


@login_required
def admin_users_list(request):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    users = User.objects.select_related('profile').annotate(
        applications_count=Count('application', distinct=True),
        offers_count=Count('internshipoffer', distinct=True),
    ).order_by('-date_joined')

    return render(request, 'accounts/admin_users_list.html', {
        'users': users,
    })


@login_required
@never_cache
def admin_user_edit(request, pk):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    edited_user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if User.objects.exclude(pk=edited_user.pk).filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe deja.")
            return redirect('admin_user_edit', pk=edited_user.pk)

        edited_user.username = username
        edited_user.email = email
        edited_user.first_name = request.POST.get('first_name', '').strip()
        edited_user.last_name = request.POST.get('last_name', '').strip()
        edited_user.is_active = request.POST.get('is_active') == 'on'
        edited_user.is_staff = request.POST.get('is_staff') == 'on'
        edited_user.save()

        messages.success(request, "Utilisateur modifie avec succes.")
        return redirect('admin_users_list')

    return render(request, 'accounts/admin_user_edit.html', {
        'edited_user': edited_user,
    })


@login_required
def admin_profiles_list(request):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    profiles = Profile.objects.select_related('user').order_by('role', 'full_name')

    return render(request, 'accounts/admin_profiles_list.html', {
        'profiles': profiles,
    })


@login_required
@never_cache
def admin_profile_edit(request, pk):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    profile = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        profile.role = request.POST.get('role', profile.role)
        profile.full_name = request.POST.get('full_name', '').strip()
        profile.phone = request.POST.get('phone', '').strip()
        profile.field = request.POST.get('field', '').strip()
        profile.study_level = request.POST.get('study_level', '').strip()
        profile.skills = request.POST.get('skills', '').strip()
        profile.company_name = request.POST.get('company_name', '').strip()
        profile.sector = request.POST.get('sector', '').strip()
        profile.address = request.POST.get('address', '').strip()
        profile.description = request.POST.get('description', '').strip()

        if request.FILES.get('cv'):
            profile.cv = request.FILES.get('cv')

        profile.save()
        messages.success(request, "Profil modifie avec succes.")
        return redirect('admin_profiles_list')

    return render(request, 'accounts/admin_profile_edit.html', {
        'profile': profile,
    })


@login_required
def admin_offers_list(request):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    offers = InternshipOffer.objects.select_related('company', 'company__profile').order_by('-created_at')

    return render(request, 'accounts/admin_offers_list.html', {
        'offers': offers,
    })


@login_required
@never_cache
def admin_offer_edit(request, pk):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    offer = get_object_or_404(InternshipOffer, pk=pk)
    companies = User.objects.filter(profile__role='company').select_related('profile').order_by('profile__company_name', 'username')

    if request.method == 'POST':
        company_id = request.POST.get('company')
        offer.company = get_object_or_404(User, pk=company_id, profile__role='company')
        offer.title = request.POST.get('title', '').strip()
        offer.description = request.POST.get('description', '').strip()
        offer.domain = request.POST.get('domain', '').strip()
        offer.required_skills = request.POST.get('required_skills', '').strip()
        offer.duration = request.POST.get('duration', '').strip()
        offer.location = request.POST.get('location', '').strip()
        offer.internship_type = request.POST.get('internship_type', 'presentiel')
        offer.deadline = request.POST.get('deadline')
        offer.status = request.POST.get('status', 'open')
        offer.save()

        messages.success(request, "Offre modifiee avec succes.")
        return redirect('admin_offers_list')

    return render(request, 'accounts/admin_offer_edit.html', {
        'offer': offer,
        'companies': companies,
    })


@login_required
def admin_applications_list(request):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    applications = Application.objects.select_related(
        'student',
        'student__profile',
        'offer',
        'offer__company',
        'offer__company__profile',
    ).order_by('-created_at')

    return render(request, 'accounts/admin_applications_list.html', {
        'applications': applications,
    })


@login_required
@never_cache
def admin_application_edit(request, pk):
    admin_redirect = require_admin(request)
    if admin_redirect:
        return admin_redirect

    application = get_object_or_404(Application, pk=pk)
    students = User.objects.filter(profile__role='student').select_related('profile').order_by('profile__full_name', 'username')
    offers = InternshipOffer.objects.select_related('company', 'company__profile').order_by('-created_at')

    if request.method == 'POST':
        student_id = request.POST.get('student')
        offer_id = request.POST.get('offer')
        application.student = get_object_or_404(User, pk=student_id, profile__role='student')
        application.offer = get_object_or_404(InternshipOffer, pk=offer_id)
        application.message = request.POST.get('message', '').strip()
        application.status = request.POST.get('status', 'pending')

        if request.FILES.get('cv'):
            application.cv = request.FILES.get('cv')

        try:
            application.save()
        except IntegrityError:
            messages.error(request, "Une candidature existe deja pour cet etudiant et cette offre.")
            return redirect('admin_application_edit', pk=application.pk)

        messages.success(request, "Candidature modifiee avec succes.")
        return redirect('admin_applications_list')

    return render(request, 'accounts/admin_application_edit.html', {
        'application': application,
        'students': students,
        'offers': offers,
    })
