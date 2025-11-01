from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_students, name='list_students'),
    path('create/', views.create_student, name='create_student'),
    path('<int:pk>/', views.get_student, name='get_student'),
    path('<int:pk>/update/', views.update_student, name='update_student'),
    path('<int:pk>/delete/', views.delete_student, name='delete_student'),
]
