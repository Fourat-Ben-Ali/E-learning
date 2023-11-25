from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/',  UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    path('students/', StudentCreateView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view(), name='student-detail'),

    path('tutors/', TutorCreateView.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', TutorRetrieveUpdateDestroyView.as_view(), name='tutor-detail'),

    path('admins/', AdminCreateView.as_view(), name='admin-list'),
    path('admins/<int:pk>/', AdminRetrieveUpdateDestroyView.as_view(), name='admin-detail'),

    path('courses/', CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),

    path('materials/', MaterialListCreateView.as_view(), name='material-list'),
    path('materials/<int:pk>/', MaterialRetrieveUpdateDestroyView.as_view(), name='material-detail'),

    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentRetrieveUpdateDestroyView.as_view(), name='enrollment-detail'),

    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/', AssignmentRetrieveUpdateDestroyView.as_view(), name='assignment-detail'),

    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', SubmissionRetrieveUpdateDestroyView.as_view(), name='submission-detail'),

    path('grades/', GradeListCreateView.as_view(), name='grade-list'),
    path('grades/<int:pk>/', GradeRetrieveUpdateDestroyView.as_view(), name='grade-detail'),

    path('interaction-history/', InteractionHistoryListCreateView.as_view(), name='interaction-history-list'),
    path('interaction-history/<int:pk>/', InteractionHistoryRetrieveUpdateDestroyView.as_view(), name='interaction-history-detail'),

    path('reading-state/', ReadingStateListCreateView.as_view(), name='reading-state-list'),
    path('reading-state/<int:pk>/', ReadingStateRetrieveUpdateDestroyView.as_view(), name='reading-state-detail'),
]
