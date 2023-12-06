from django.urls import path
from . import views


urlpatterns = [
    
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_form, name='enroll_form'),
    path('courses/', views.course_list, name='course_liste'),
    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('course_already_registered/', views.course_already_registered_view, name='course_already_registered_page'),
    path('enrollment/success/', views.enrollement_success, name='enrollement_success'),
    path('dashbord/', views.dashboard, name='dashbord'),
]
