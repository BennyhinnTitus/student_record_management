from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer

# ✅ 1. Welcome Endpoint
@require_GET
def welcome(request):
    return JsonResponse({"message": "Welcome to the Student Management API 🎓"}, status=200)


# ✅ 2. List All Students
@require_GET
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


# ✅ 3. Add New Student
@csrf_exempt
@require_POST
def add_student(request):
    data = JSONParser().parse(request)
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


# ✅ 4. Update Student (Full or Partial)
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_student(request):
    data = JSONParser().parse(request)
    try:
        student = Student.objects.get(id=data.get('id'))
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    partial = request.method == "PATCH"
    serializer = StudentSerializer(student, data=data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        msg = "Student fully updated ✅" if not partial else "Student partially updated ⚙️"
        return JsonResponse({"message": msg, "data": serializer.data}, status=200)
    return JsonResponse(serializer.errors, status=400)


# ✅ 5. Delete Student
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_student(request):
    data = JSONParser().parse(request)
    try:
        student = Student.objects.get(id=data.get('id'))
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully 🗑️'}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
