from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Student
from .serializers import StudentSerializer
from .utils import generate_jwt 

class StudentLogin(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Email y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'No existe un estudiante con ese email'}, status=status.HTTP_404_NOT_FOUND)

        if not student.check_password(password):
            return Response({'error': 'La contraseña es incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generar el JWT
        token = generate_jwt(email, password)

        # Devolver el JWT en la respuesta
        response =  Response({'token': token},status=status.HTTP_200_OK)
        response['Authorization'] = f'Bearer {token}'
        return response
