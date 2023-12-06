from django.shortcuts import render, get_object_or_404, redirect
from .forms import EnrollmentForm
from platform_app.models import Course, Student, Enrollment
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse

def dashboard(request):
    return render(request, 'students_dashbord.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_liste.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment_count = Enrollment.objects.filter(course=course).count()
    remaining_capacity = course.enrollement_capacity - enrollment_count
    professor_name = course.tutor.first_name

    if remaining_capacity > 0:
        if request.method == 'POST':
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                enrollment = form.save(commit=False)
                student = request.user.student
                enrollment.student = student
                enrollment.course = course
                enrollment.save()
                return redirect('course_detail', course_id=course_id)
        else:
            form = EnrollmentForm()
    else:
        form = None

    return render(
        request,
        'course_detail.html',
        {
            'course': course,
            'remaining_capacity': remaining_capacity,
            'professor_name': professor_name,
            'form': form
        }
    )

def enroll_form(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            # Traitement des données du formulaire
            return HttpResponseRedirect('/confirmation/')  # Redirection après inscription
    else:
        form = EnrollmentForm()

    return render(request, 'enroll_form.html', {'form': form, 'course': course})

def enroll_student(request):
    course_id = request.POST.get('course_id')
    context = {'course_already_registered': False} 
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            
            try:
                user = Student.objects.get(username=username)
                student = user.student
                course = Course.objects.get(id=course_id)

                # Vérifier si l'étudiant est déjà inscrit dans ce cours
                if Enrollment.objects.filter(student=student, course=course).exists():
                    messages.error(request, 'Vous êtes déjà inscrit à ce cours !')
                    messages.error(request, 'Vous êtes déjà inscrit à ce cours !')
                    return redirect('course_already_registered_page')
                else:
                    Enrollment.objects.create(student=student, course=course)
                    messages.success(request, 'Inscription réussie !')

                    return redirect('enrollement_success')  # Rediriger vers la liste des cours après inscription
            
            except Student.DoesNotExist:
                messages.error(request, 'Utilisateur non trouvé !')
                return render(request, 'student_not_found.html')
            except Course.DoesNotExist:
                messages.error(request, 'Cours non trouvé !')
                return render(request, 'course_not_found.html')
    else:
        form = EnrollmentForm()

    return render(request, 'enroll_form.html', {'form': form})

def course_already_registered_view(request):
    return render(request, 'course_already_registered.html')

def enrollement_success(request):
    return render(request, 'enrollment_success.html')
