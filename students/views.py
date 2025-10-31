from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

# ViewSet = handles all CRUD (Create, Read, Update, Delete)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()           # what data to show
    serializer_class = StudentSerializer       # how to convert data (JSON <-> Python)
