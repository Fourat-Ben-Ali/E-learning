from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from platform_app.models import (  # Importe tes modèles depuis platform_app
    Enrollment,
    Course,
    Material,
    Grade,
    Submission,
    InteractionHistory,
    Assignment,
    Student,
    Tutor,
    Admin,
)
from platform_app.serializers import (  # Assure-toi d'avoir les bons chemins pour les serializers
    EnrollmentSerializer,
    CourseSerializer,
    MaterialSerializer,
    GradeSerializer,
    SubmissionSerializer,
    InteractionHistorySerializer,
)
from rest_framework.authtoken.models import Token

# Assure-toi d'importer correctement tous tes modèles et serializers

# Adaptation des vues à tes modèles de platform_app

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    # Add other viewset methods as needed

# Fais de même pour les autres vues (MaterialsViewSet, CoursesViewSet, GradesViewSet, SubmissionViewSet, HistoryViewSet)
