from rest_framework import serializers   # Import DRF serializer tools
from .models import Student              # Import your model

# Create a serializer for Student model
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student                  # The model this serializer is for
        fields = '__all__'               # Include all model fields (id, name, age, cgpa, attendance)
