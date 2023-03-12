from django.db import models

# Modelos del proyecto

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password as django_check_password



class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    registration_number = models.CharField(max_length=10, unique=True)
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])
    
    def clean(self):
        super().clean()
        if len(self.registration_number) != 10:
            raise ValidationError('El número de registro debe tener exactamente 10 caracteres.')
        
    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField() # Fecha en la que se llevará a cabo el examen
    class Meta:
        verbose_name = 'Examen'
        verbose_name_plural = 'Examenes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exam_detail', args=[str(self.id)])


class Question(models.Model):
    exam = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text  = models.TextField()
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return self.question_text
    
    def get_absolute_url(self):
        return reverse('question_detail', args=[str(self.id)])

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('answer_detail', args=[str(self.id)])
