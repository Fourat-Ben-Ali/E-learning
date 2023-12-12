from django.urls import path
from .views import StudentRegisterView, StudentLoginView,StudentLogoutView,TutorLoginView
from . import views

urlpatterns = [
    path('login/',  StudentLoginView.as_view(), name='login'),
    path('logout/', StudentLogoutView.as_view(), name='logout'),
    path('authentication/register/', StudentRegisterView.as_view(), name='student_register'),
    path('tutor_login/', TutorLoginView.as_view(), name='tutor_login'),
    path('', views.home, name='home'),
    
]