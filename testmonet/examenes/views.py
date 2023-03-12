
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomJWTSerializer


class CustomObtainJSONWebToken(TokenObtainPairView):
    serializer_class = CustomJWTSerializer