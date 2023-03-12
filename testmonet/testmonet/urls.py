from django.urls import path
from examenes.views import StudentTokenObtainPairView

urlpatterns = [
    path('token/', StudentTokenObtainPairView.as_view(), name='token_obtain_pair'),
]