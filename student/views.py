from django.shortcuts import render, get_object_or_404, redirect
from .forms import EnrollmentForm
from platform_app.models import Course, Student, Enrollment,Material,Assignment,Submission,Grade
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

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

def student_courses(request, student_id):
    # Récupérer l'objet Student ou renvoyer une erreur 404 si l'étudiant n'existe pas
    student = get_object_or_404(Student, id=student_id)

    # Récupérer tous les enregistrements d'inscription pour cet étudiant
    enrollments = Enrollment.objects.filter(student=student)
    print(enrollments) 
    # Récupérer la liste des cours à partir des enregistrements d'inscription
    courses = [enrollment.course for enrollment in enrollments]
    print(courses) 
    return render(request, 'student_courses.html', {'student': student, 'courses': courses})
def course_materials(request, course_id ):
    course = get_object_or_404(Course, id=course_id)
    materials = Material.objects.filter(course=course)
    assignments = Assignment.objects.filter(course=course)
    
  
    return render(request, 'course_materials.html', {'course': course, 'materials': materials,'assignments': assignments})
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        username = request.POST['username']
        submission_content = request.POST['submission_content']
        pdf_file = request.FILES['pdf']
        current_student = Student.objects.get(username=username)

        if assignment.due_date < timezone.now().date():
            return HttpResponse("La date limite pour ce devoir est déjà passée.")
        else:
            previous_submission = Submission.objects.filter(student=current_student, assignment=assignment).first()

            if previous_submission:
                return HttpResponse("Vous avez déjà soumis ce devoir.")
            else:
                submission = Submission.objects.create(
                    student=current_student,
                    assignment=assignment,
                    submission_content=submission_content,
                    pdf=pdf_file
                )
                submission.save()


                return render(request, 'submission_form.html', {'assignment': assignment})
    else:
        return render(request, 'submission_form.html', {'assignment': assignment})
    
def grade_detail_view(request, student_id):
    # Récupérer tous les grades de l'étudiant spécifié
    student_grades = Grade.objects.filter(student_id=student_id)

    context = {
        'student_id': student_id,
        'student_grades': student_grades,
    }
    return render(request, 'grade_detail.html', context)