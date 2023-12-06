from django.db import models
from django.core.validators import EmailValidator

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()])
    date_joined = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['date_joined']
        verbose_name = 'Utilisateur'
        unique_together = ['email', 'username']
        
"""class Student(User):
    # Ajouter les champs spécifiques à l'étudiant ici, s'il y en a
    enrolled_courses = models.ManyToManyField(Course, related_name='enrolled_students')

    def __str__(self):
        return self.username"""
    
class Tutor(User):
    def __str__(self):
        return self.username
    
class Admin(User):
    def __str__(self):
        return self.username    
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255) 
    enrollement_capacity = models.IntegerField(default=25)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class Student(User):
    # Ajouter les champs spécifiques à l'étudiant ici, s'il y en a
    enrolled_courses = models.ManyToManyField(Course, related_name='enrolled_students')

    def __str__(self):
        return self.username

class Material(models.Model):
    DOCUMENT_TYPES = [
        ('PDF', 'PDF'),
        ('DOC', 'Document'),
        ('PPT', 'Presentation'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPES)

    def __str__(self):
        return self.title
    

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now=True)

    def __str__(self):
     return self.student

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    due_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_content = models.TextField()
    submission_date = models.DateField(auto_now=True)
    def __str__(self):
        return f"submission by{self.student.username} for {self.assignment.title}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    feedback = models.CharField(max_length=255)
    def __str__(self):
        return f"Grade for {self.student.username} on {self.assignment.title}"

    
class InteractionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=100)
    interaction_date = models.DateField(auto_now=True)
    def __str__(self):
        return f"Interaction: {self.interaction_type} by {self.student.username} on {self.material.title}"
    
class ReadingState(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    read_state = models.FloatField()
    last_read = models.DateField(auto_now=True)
    def __str__(self):
        return f"Reading {self.read_state} by {self.student.username} on {self.material.title}"