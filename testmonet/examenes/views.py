from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer
from .utils import generate_jwt 

from rest_framework.permissions import IsAuthenticated


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

"""
class RegisterExamAnswer(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ExamAnswerSerializer(data=request.data)
        if serializer.is_valid():
            student = request.user
            exam_id = serializer.validated_data['exam_id']
            answers = serializer.validated_data['answers']
            exam = Exam.objects.get(id=exam_id)

            # Verificar que el examen esté disponible
            if not exam.is_available():
                return Response({'error': 'Este examen ya no está disponible'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que el estudiante no haya respondido el examen antes
            if student.exam_answers.filter(exam=exam).exists():
                return Response({'error': 'Ya has respondido este examen'}, status=status.HTTP_400_BAD_REQUEST)

            # Guardar las respuestas del examen
            exam_answer = ExamAnswer.objects.create(student=student, exam=exam, answers=answers)

            # Retornar la respuesta con el id del examen registrado
            response_data = {'id': exam_answer.id}
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        """