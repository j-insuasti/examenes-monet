from django.urls import path
from django.contrib import admin
from examenes.views import StudentLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', StudentLogin.as_view(), name='token_obtain_pair'),
]

