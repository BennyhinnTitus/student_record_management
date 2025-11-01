from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome),
    path('list/', views.list_students),
    path('add/', views.add_student),
    path('update/', views.update_student),
    path('delete/', views.delete_student),
]
