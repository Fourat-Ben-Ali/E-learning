from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
      path('tutor_courses/<int:tutor_id>/', views.tutor_courses, name='tutor_courses'),
      path('manage_course/<int:course_id>/', views.manage_course, name='manage_course'),
      path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
      path('tutor_dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
      path('add_material_to_course/<int:course_id>/', views.add_material_to_course, name='add_material_to_course'),
      path('tutor_dashboard/<int:tutor_id>/', views.tutor_dashboard, name='tutor_dashboard'),
      path('view_course_materials/<int:course_id>/', views.view_course_materials, name='view_course_materials'),
      path('delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
      path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
      path('course/<int:course_id>/students/', views.course_students, name='course_students'),
      path('add_assignment_to_course/<int:course_id>/', views.add_assignment_to_course, name='add_assignment_to_course'),
      path('tutor/<int:tutor_id>/add_course/', views.add_course, name='add_course'),
      path('view_submissions/<int:course_id>/', views.view_submissions, name='view_submissions'),
      path('add_grade_to_submission/<int:assignment_id>/', views.add_grade_to_submission, name='add_grade_to_submission'),
      path('grade_submission/<int:submission_id>/', views.add_grade_to_submission, name='grade_submission'),
      path('tutor/tutor_courses/<int:tutor_id>/',views.tutor_courses, name='tutor_courses')
]
