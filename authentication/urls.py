from django.urls import path
from .views import StudentRegisterView, StudentLoginView,StudentLogoutView

urlpatterns = [
    path('login/',  StudentLoginView.as_view(), name='login'),
    path('logout/', StudentLogoutView.as_view(), name='logout'),
   path('authentication/register/', StudentRegisterView.as_view(), name='student_register'),
    # Other URL patterns
    
]