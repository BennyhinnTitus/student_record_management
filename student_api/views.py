from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer, CourseDetailSerializer


# ===================================================
# 🧠 PART 1 — APIView IMPLEMENTATION (Manual CRUD)
# ===================================================

class StudentAPIView(APIView):
    """Handles GET (list) and POST (create) for students."""

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailAPIView(APIView):
    """Handles GET, PUT, PATCH, DELETE for a single student."""

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ===================================================
# 🎓 COURSE APIViews
# ===================================================

class CourseAPIView(APIView):
    """Handles GET and POST for courses."""

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
    """Retrieve a course with related students."""

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)


class StudentsByCourseCodeAPIView(APIView):
    """List students filtered by course code."""
    def get(self, request, course_code):
        students = Student.objects.filter(course__course_code=course_code)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


# ===================================================
# 🧠 PART 2 — GENERIC VIEWS IMPLEMENTATION
# ===================================================

class StudentListCreateView(generics.ListCreateAPIView):
    """GET: List all students, POST: Create new student"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE single student"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCreateOnlyView(generics.CreateAPIView):
    """POST only"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentListOnlyView(generics.ListAPIView):
    """GET only"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ===================================================
# 🎓 GENERIC COURSE VIEWS
# ===================================================

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# ===================================================
# 🔍 PART 3 — LOOKUP FIELD DEMONSTRATIONS
# ===================================================

# Task 2: lookup_field=email
class StudentByEmailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "email"         # field to look up by
    lookup_url_kwarg = "email"     # matches <str:email> in URL


# Task 3: filter by course code
class StudentByCourseView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        course_code = self.kwargs.get("course_code")
        return Student.objects.filter(course__course_code=course_code)
