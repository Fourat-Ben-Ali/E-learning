from django.urls import path
from . import views,student


urlpatterns = [
    
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_form, name='enroll_form'),
    path('courses/', views.course_list, name='course_liste'),
    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('course_already_registered/', views.course_already_registered_view, name='course_already_registered_page'),
    path('enrollment/success/', views.enrollement_success, name='enrollement_success'),
    path('dashbord/', views.dashboard, name='dashbord'),
    path('student/student_courses/<int:student_id>/', views.student_courses, name='student_courses'),
    path('enrollments/', student.EnrollmentViewSet.as_view({'post': 'create'}), name='enrollment-list'),
    path('course/<int:course_id>/materials/', views.course_materials, name='course_materials'),
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('grades/<int:student_id>/', views.grade_detail_view, name='grades_student'),
]
