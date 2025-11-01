from rest_framework import serializers
from .models import Student
from django.core.exceptions import ValidationError
import re


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['enrollment_date']

    # 1️⃣ Name Validation
    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Name should only contain letters and spaces.")
        return value

    # 2️⃣ Age Validation
    def validate_age(self, value):
        if value < 18 or value > 60:
            raise serializers.ValidationError("Age must be between 18 and 60.")
        return value

    # 3️⃣ Email Validation
    def validate_email(self, value):
        allowed_domains = ('.edu', '.ac.in', '.edu.in')
        if not value.endswith(allowed_domains):
            raise serializers.ValidationError("Email must end with .edu, .ac.in, or .edu.in.")
        return value

    # 4️⃣ Phone Number Validation
    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Phone number should contain only digits.")
            if len(value) != 10:
                raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

    # 5️⃣ Multi-field Validation
    def validate(self, data):
        course = data.get('course')
        age = data.get('age')

        if course == "Computer Science" and age < 20:
            raise serializers.ValidationError("Students in Computer Science must be at least 20 years old.")
        if course == "Data Science" and age < 22:
            raise serializers.ValidationError("Students in Data Science must be at least 22 years old.")
        return data
