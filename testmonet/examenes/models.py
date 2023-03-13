from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.hashers import  make_password, check_password
from rest_framework.serializers import ValidationError
# Modelos del proyecto
import hashlib
from django.core.validators import EmailValidator


class Student(models.Model):
    user = models.OneToOneField('auth.User',verbose_name='Nombre del usuario', on_delete=models.CASCADE, related_name='student', null=True, blank=True)
    email = models.CharField(verbose_name='Correo del estudiante',max_length=100, validators=[EmailValidator()])
    registration_number = models.CharField(verbose_name='Identificador del estudiante',max_length=10, unique=True)
    password_hash = models.CharField(verbose_name='Contraseña del estudiante', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])

    def clean(self):
        super().clean()
        if len(self.registration_number) != 10:
            raise ValidationError('El número de registro debe tener exactamente 10 caracteres.')

    def set_password(self, raw_password):
        salt = hashlib.sha256(str.encode(self.user.email)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', str.encode(raw_password), salt, 100000)
        pwdhash = pwdhash.hex()
        self.user.password = make_password(pwdhash)
    #Valida la con
    def check_password(self, raw_password):
        return check_password(raw_password, self.user.password)

    def save(self, *args, **kwargs):
        if self.user_id is None:
            self.user = User.objects.create()
            self.set_password(self.registration_number)  # Llamada a set_password
        super().save(*args, **kwargs)


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
    question_text = models.TextField()
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
