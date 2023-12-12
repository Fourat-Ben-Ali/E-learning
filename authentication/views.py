from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from django.conf import settings
from platform_app.models import Student,Tutor
from platform_app.serializers import StudentSerializer  
from django.shortcuts import render
from student.views import course_list
from django.shortcuts import redirect



class StudentRegisterView(APIView):
    def get(self, request):
        return render(request, 'student_register.html')  # Afficher le formulaire HTML
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return render(request, 'student_login.html')
      
class StudentLoginView(APIView):
    def get(self, request):
        return render(request, 'student_login.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Recherche de l'étudiant en utilisant l'email
        student = Student.objects.filter(email=email).first()

        if student is None:
           raise AuthenticationFailed('User not found')

        # Vérification du mot de passe
        if password != student.password:
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': student.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # Encodage du token JWT en utilisant la clé secrète de Django
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        student_id=student.id
        # Rendre la template HTML pour l'utilisateur
       # return render(request, 'course_liste.html', {'jwt': token})
        return render(request, 'students_dashbord.html', {'student_id': student_id}) 
    
class StudentLogoutView(APIView):
    def post(self, request):
        jwt_token = request.data.get('jwt')  # Récupérer le token JWT depuis le corps de la requête JSON

        if not jwt_token:
            return JsonResponse({'message': 'Token not provided'}, status=400)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Session expired. Please log in again.'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token. Please log in again.'}, status=401)

        return JsonResponse({'message': 'Logout successful'})
    

class TutorLoginView(APIView):
    def get(self, request):
        return render(request, 'tutor_login.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Recherche du tuteur en utilisant l'email
        tutor = Tutor.objects.filter(email=email).first()

        if tutor is None or tutor.password != password:
            raise AuthenticationFailed('Invalid email or password')

        payload = {
            'id': tutor.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # Encodage du token JWT en utilisant la clé secrète de Django
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return render(request, 'tutor_dashboard.html', {'jwt': token, 'tutor_id': tutor.id, 'tutor_name': tutor.username})

def home(request):
     return render(request, 'index.html')