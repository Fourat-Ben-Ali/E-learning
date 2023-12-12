
from django.shortcuts import render, get_object_or_404, redirect
from platform_app.models import Course, Tutor, Material,Enrollment,Assignment,Submission,Grade
from .forms import CourseForm,AssignmentForm
from django.http import HttpResponseRedirect

def tutor_dashboard(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    courses = Course.objects.filter(tutor=tutor)
    tutor_name = tutor.first_name
    return render(request, 'tutor_dashboard.html', {'courses': courses, 'tutor': tutor, 'tutor_id': tutor_id ,'tutor_name': tutor_name})


def tutor_courses(request, tutor_id):
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    courses = Course.objects.filter(tutor_id=tutor_id)
     
    return render(request, 'tutor_courses.html', {'courses': courses, 'tutor': tutor})

def manage_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST' and 'delete_course' in request.POST:
        tutor_id = course.tutor_id
        course.delete()
        return redirect('tutor_dashboard', tutor_id=tutor_id)

    return render(request, 'manage_course.html', {'course': course})

def add_material_to_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        document_type = request.POST.get('document_type')
        file = request.FILES['file'] 
        print('file exit')
        new_material = Material.objects.create(
            title=title,
            content=content,
            document_type=document_type,
            course=course,
            file=file
        )

        return render(request, 'material_added.html', {'material': new_material, 'course': course})

    return render(request, 'add_material_to_course.html', {'course': course})

def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    tutor_id = course.tutor_id

    if request.method == 'POST':
        course.delete()
        return redirect('tutor_dashboard', tutor_id=tutor_id)

    # Si ce n'est pas une requête POST, peut-être rediriger ailleurs ou lever une erreur
    return redirect('some_other_view')

def view_course_materials(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    materials = Material.objects.filter(course=course)
    
    return render(request, 'view_course_materials.html', {'course': course, 'materials': materials})
def delete_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    # Vérifiez si la requête est une méthode POST pour supprimer le matériel
    if request.method == 'POST':
        material.delete()
    return redirect('view_course_materials', course_id=material.course.id)


def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            # Redirigez vers la page du cours mis à jour ou toute autre page souhaitée.
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'edit_course.html', {'form': form, 'course': course})  

def course_students(request, course_id):
    course = Course.objects.get(pk=course_id)
    enrolled_students = Enrollment.objects.filter(course=course)
    students = [enrollment.student for enrollment in enrolled_students]
 
    return render(request, 'course_students.html', {'course': course, 'students': students})  




def add_assignment_to_course(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            Assignment = form.save(commit=False)
            Assignment.course = course
            Assignment.save()
            
    else:
        form = AssignmentForm()

    return render(request, 'add_assignment.html', {'form': form, 'course': course})
def add_course(request, tutor_id):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            # Assign the course to the tutor using tutor_id
            course.tutor_id = tutor_id
            course.save()
            return redirect('tutor_dashboard')  # Rediriger vers le tableau de bord du tuteur après l'ajout du cours
    else:
        form = CourseForm()
    
    return render(request, 'add_course.html', {'form': form})


def view_submissions(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    assignments = Assignment.objects.filter(course=course)
    submissions = Submission.objects.filter(assignment__in=assignments)

    return render(
        request,
        'view_submissions.html',
        {'course': course, 'assignments': assignments, 'submissions': submissions}
    )


from django.urls import reverse
def add_grade_to_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    student = submission.student
    assignment = submission.assignment

    # Check if a grade already exists for the student and assignment
    existing_grade = Grade.objects.filter(student=student, assignment=assignment).first()

    if request.method == 'POST':
        grade_value = request.POST.get('grade')
        feedback = request.POST.get('feedback')

        # If a grade already exists, prevent creating a new one
        if existing_grade:
            # Redirect or show an error message to indicate a grade already exists
            return HttpResponseRedirect(reverse('view_submissions', args=[assignment.course.id]))

        # If no grade exists, create a new grade
        Grade.objects.create(student=student, assignment=assignment, grade=grade_value, feedback=feedback)

        # Redirect to the 'view_submissions' URL pattern
        return HttpResponseRedirect(reverse('view_submissions', args=[assignment.course.id]))

    return render(request, 'add_grade_to_submission.html', {'submission': submission})