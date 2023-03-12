from django.db import models

# Modelos del proyecto

from django.db import models
from django.urls import reverse


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    registration_number = models.CharField(max_length=10, unique=True)
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])


class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    class Meta:
        verbose_name = 'Examen'
        verbose_name_plural = 'Examenes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exam_detail', args=[str(self.id)])


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return self.text
    
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
