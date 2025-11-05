from django.urls import path
from .views import (
    # 🧠 Part 1 – APIView-based
    StudentAPIView,
    StudentDetailAPIView,
    CourseAPIView,
    CourseDetailAPIView,
    StudentsByCourseCodeAPIView,

    # 🧠 Part 2 – Generic Views
    StudentListCreateView,
    StudentDetailView,
    StudentCreateOnlyView,
    StudentListOnlyView,

    # 🎓 Generic Courses
    CourseListCreateView,
    CourseDetailView,

    # 🔍 Part 3 – Custom Lookups
    StudentByEmailView,
    StudentByCourseView,

    # 🧩 New — User Registration
    RegisterUserAPIView,
    CurrentUserAPIView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ==================================================
    # 🧠 PART 1 — APIView Endpoints
    # ==================================================
    path('students/', StudentAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),

    path('courses/', CourseAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('courses/<str:course_code>/students/', StudentsByCourseCodeAPIView.as_view(), name='students-by-course-code'),

    # ==================================================
    # 🧠 PART 2 — GENERIC VIEW ENDPOINTS
    # ==================================================
    path('students-generic/', StudentListCreateView.as_view(), name='student-list-create-generic'),
    path('students-generic/<int:pk>/', StudentDetailView.as_view(), name='student-detail-generic'),
    path('students-create-only/', StudentCreateOnlyView.as_view(), name='student-create-only'),
    path('students-list-only/', StudentListOnlyView.as_view(), name='student-list-only'),

    # ==================================================
    # 🔍 PART 3 — LOOKUP FIELD DEMOS
    # ==================================================
    path('students/email/<str:email>/', StudentByEmailView.as_view(), name='student-by-email'),
    path('students/course/<str:course_code>/', StudentByCourseView.as_view(), name='student-by-course'),

    # ==================================================
    # 🎓 GENERIC COURSE ENDPOINTS
    # ==================================================
    path('courses-generic/', CourseListCreateView.as_view(), name='course-list-create-generic'),
    path('courses-generic/<int:pk>/', CourseDetailView.as_view(), name='course-detail-generic'),

    # ==================================================
    # 🧩 NEW — USER REGISTRATION ENDPOINT
    # ==================================================
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('users/me/', CurrentUserAPIView.as_view(), name='current-user'),

    # Token auth (DRF built-in)
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),

    # JWT auth (simplejwt)
    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
