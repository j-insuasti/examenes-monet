from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Student
from .utils import generate_jwt


class StudentLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(email='hola@hotmail.com', registration_number='1234567890')
        self.student.set_password('contrasena123')
        self.student.save()

    def test_valid_login(self):
        url = reverse('token_obtain_pair')
        data = {'email': self.student.email, 'password': 'contrasena123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Authorization' in response.headers)

    def test_missing_credentials(self):
        url = reverse('token_obtain_pair')
        data = {'email': self.student.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)

    def test_invalid_email(self):
        url = reverse('token_obtain_pair')
        data = {'email': 'invalidemail', 'password': 'contrasena123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)

    def test_incorrect_password(self):
        url = reverse('token_obtain_pair')
        data = {'email': self.student.email, 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('error' in response.data)

    def test_valid_jwt(self):
        jwt = generate_jwt(self.student.email, 'contrasena123')
        url = reverse('token_obtain_pair')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt}')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.student.email)

