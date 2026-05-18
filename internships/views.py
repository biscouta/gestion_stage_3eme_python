from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from .models import InternshipOffer


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
def student_internship_list(request):
    if get_user_role(request.user) != 'student':
        messages.error(request, "Seuls les etudiants peuvent consulter cette page.")
        return redirect_by_role(request.user)

    query = request.GET.get('q', '').strip()
    offers = InternshipOffer.objects.filter(status='open').order_by('-created_at')

    if query:
        offers = offers.filter(
            Q(title__icontains=query)
            | Q(domain__icontains=query)
            | Q(location__icontains=query)
            | Q(required_skills__icontains=query)
        )

    return render(request, 'internships/student_internship_list.html', {
        'offers': offers,
        'query': query,
    })


@login_required
def company_internship_list(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent consulter cette page.")
        return redirect_by_role(request.user)

    offers = InternshipOffer.objects.filter(company=request.user).order_by('-created_at')
    return render(request, 'internships/company_internship_list.html', {
        'offers': offers,
    })


@login_required
def internship_detail(request, pk):
    offer = get_object_or_404(InternshipOffer, pk=pk)

    if get_user_role(request.user) == 'company' and offer.company != request.user:
        messages.error(request, "Vous ne pouvez consulter que vos propres offres.")
        return redirect('company_internship_list')

    return render(request, 'internships/internship_detail.html', {
        'offer': offer,
    })


@login_required
@never_cache
def create_internship(request):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent creer une offre.")
        return redirect_by_role(request.user)

    if request.method == 'POST':
        InternshipOffer.objects.create(
            company=request.user,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            domain=request.POST.get('domain', ''),
            required_skills=request.POST.get('required_skills', ''),
            duration=request.POST.get('duration', ''),
            location=request.POST.get('location', ''),
            internship_type=request.POST.get('internship_type', 'presentiel'),
            deadline=request.POST.get('deadline'),
            status=request.POST.get('status', 'open'),
        )

        messages.success(request, "Offre de stage creee avec succes.")
        return redirect('company_internship_list')

    return render(request, 'internships/internship_form.html')


@login_required
@never_cache
def update_internship(request, pk):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent modifier une offre.")
        return redirect_by_role(request.user)

    offer = get_object_or_404(InternshipOffer, pk=pk, company=request.user)

    if request.method == 'POST':
        offer.title = request.POST.get('title', '')
        offer.description = request.POST.get('description', '')
        offer.domain = request.POST.get('domain', '')
        offer.required_skills = request.POST.get('required_skills', '')
        offer.duration = request.POST.get('duration', '')
        offer.location = request.POST.get('location', '')
        offer.internship_type = request.POST.get('internship_type', 'presentiel')
        offer.deadline = request.POST.get('deadline')
        offer.status = request.POST.get('status', 'open')
        offer.save()

        messages.success(request, "Offre de stage modifiee avec succes.")
        return redirect('company_internship_list')

    return render(request, 'internships/internship_form.html', {
        'offer': offer,
    })


@login_required
@never_cache
def delete_internship(request, pk):
    if get_user_role(request.user) != 'company':
        messages.error(request, "Seules les entreprises peuvent supprimer une offre.")
        return redirect_by_role(request.user)

    offer = get_object_or_404(InternshipOffer, pk=pk, company=request.user)

    if request.method == 'POST':
        offer.delete()
        messages.success(request, "Offre de stage supprimee avec succes.")
        return redirect('company_internship_list')

    return render(request, 'internships/delete_internship.html', {
        'offer': offer,
    })


@login_required
def supervisor_internship_list(request):
    return redirect('company_internship_list')
