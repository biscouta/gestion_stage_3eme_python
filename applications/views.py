from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from internships.models import InternshipOffer
from .models import Application


def get_user_role(user):
    profile = getattr(user, 'profile', None)
    return profile.role if profile else None


def redirect_by_role(user):
    role = get_user_role(user)

    if role == 'student':
        return redirect('student_dashboard')
    if role == 'company':
        return redirect('company_dashboard')
    return redirect('login')


@login_required
@never_cache
def apply_for_internship(request, pk):
    if get_user_role(request.user) != 'student':
        messages.error(request, "Seuls les etudiants peuvent postuler.")
        return redirect_by_role(request.user)

    offer = get_object_or_404(InternshipOffer, pk=pk, status='open')

    if Application.objects.filter(student=request.user, offer=offer).exists():
        messages.error(request, "Vous avez deja postule a cette offre.")
        return redirect('student_internship_list')

    if request.method == 'POST':
        try:
            Application.objects.create(
                student=request.user,
                offer=offer,
                message=request.POST.get('message', ''),
                cv=request.FILES.get('cv'),
            )
        except IntegrityError:
            messages.error(request, "Vous avez deja postule a cette offre.")
            return redirect('student_internship_list')

        messages.success(request, "Candidature envoyee avec succes.")
        return redirect('student_applications')

    return render(request, 'applications/apply.html', {
        'offer': offer,
    })


@login_required
def student_applications(request):
    if get_user_role(request.user) != 'student':
        messages.error(request, "Seuls les etudiants peuvent consulter leurs candidatures.")
        return redirect_by_role(request.user)

    applications = Application.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'applications/student_applications.html', {
        'applications': applications,
    })


@login_required
@never_cache
def internship_applications(request, pk):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent consulter les candidatures.")
        return redirect_by_role(request.user)

    offer = get_object_or_404(InternshipOffer, pk=pk, company=request.user)
    applications = Application.objects.filter(offer=offer).order_by('-created_at')

    return render(request, 'applications/internship_applications.html', {
        'offer': offer,
        'applications': applications,
    })


@login_required
def accept_application(request, pk):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent accepter une candidature.")
        return redirect_by_role(request.user)

    application = get_object_or_404(Application, pk=pk, offer__company=request.user)
    application.status = 'accepted'
    application.save()

    messages.success(request, "Candidature acceptee.")
    return redirect('company_internship_applications', pk=application.offer.pk)


@login_required
def reject_application(request, pk):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent refuser une candidature.")
        return redirect_by_role(request.user)

    application = get_object_or_404(Application, pk=pk, offer__company=request.user)
    application.status = 'rejected'
    application.save()

    messages.success(request, "Candidature refusee.")
    return redirect('company_internship_applications', pk=application.offer.pk)
