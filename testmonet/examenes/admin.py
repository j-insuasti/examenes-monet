from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)