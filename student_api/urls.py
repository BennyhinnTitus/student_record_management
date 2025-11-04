from django.urls import path
from . import views

urlpatterns = [
    # Student CRUD
    path('students/', views.list_students),
    path('students/create/', views.create_student),
    path('students/<int:pk>/', views.get_student),
    path('students/<int:pk>/update/', views.update_student),
    path('students/<int:pk>/delete/', views.delete_student),

    # Nested Serializer Endpoints
    path('students/with-courses/', views.list_students_with_courses),
    path('courses/', views.list_courses),
    path('courses/<int:pk>/students/', views.course_detail_with_students),
    path('courses/create/', views.create_course),
    path('courses/<str:course_code>/students/', views.students_by_course_code),
]
