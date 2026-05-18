from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as auth_views
from internships import views as internship_views
from applications import views as application_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/student/', auth_views.register_student, name='register_student'),
    path('register/company/', auth_views.register_company, name='register_company'),
    path('register/supervisor/', auth_views.register_supervisor, name='register_supervisor'),

    # Student routes
    path('student/dashboard/', auth_views.student_dashboard, name='student_dashboard'),
    path('student/profile/', auth_views.student_profile, name='student_profile'),
    path('student/profile/edit/', auth_views.student_profile_edit, name='student_profile_edit'),
    path('student/applications/', application_views.student_applications, name='student_applications'),
    path('student/internships/', internship_views.student_internship_list, name='student_internship_list'),
    path('student/internships/<int:pk>/apply/', application_views.apply_for_internship, name='apply_for_internship'),

    # Company routes
    path('company/dashboard/', auth_views.company_dashboard, name='company_dashboard'),
    path('company/profile/', auth_views.company_profile, name='company_profile'),
    path('company/profile/edit/', auth_views.company_profile_edit, name='company_profile_edit'),
    path('company/internships/', internship_views.company_internship_list, name='company_internship_list'),
    path('company/internships/new/', internship_views.create_internship, name='create_internship_company'),
    path('company/internships/<int:pk>/', internship_views.internship_detail, name='company_internship_detail'),
    path('company/internships/<int:pk>/edit/', internship_views.update_internship, name='update_internship_company'),
    path('company/internships/<int:pk>/delete/', internship_views.delete_internship, name='delete_internship_company'),
    path('company/internships/<int:pk>/applications/', application_views.internship_applications, name='company_internship_applications'),
    path('company/applications/<int:pk>/accept/', application_views.accept_application, name='accept_application_company'),
    path('company/applications/<int:pk>/reject/', application_views.reject_application, name='reject_application_company'),

    # Admin custom dashboard
    path('admin-dashboard/', auth_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', auth_views.admin_users_list, name='admin_users_list'),
    path('admin-dashboard/users/<int:pk>/edit/', auth_views.admin_user_edit, name='admin_user_edit'),
    path('admin-dashboard/profiles/', auth_views.admin_profiles_list, name='admin_profiles_list'),
    path('admin-dashboard/profiles/<int:pk>/edit/', auth_views.admin_profile_edit, name='admin_profile_edit'),
    path('admin-dashboard/offers/', auth_views.admin_offers_list, name='admin_offers_list'),
    path('admin-dashboard/offers/<int:pk>/edit/', auth_views.admin_offer_edit, name='admin_offer_edit'),
    path('admin-dashboard/applications/', auth_views.admin_applications_list, name='admin_applications_list'),
    path('admin-dashboard/applications/<int:pk>/edit/', auth_views.admin_application_edit, name='admin_application_edit'),

    # Default
    path('', auth_views.login_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
