from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Student, Course
import re

# 🎓 Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_course_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Course name must be at least 3 characters long.")
        return value

    def validate_course_code(self, value):
        if Course.objects.filter(course_code=value).exists():
            raise serializers.ValidationError("Course code must be unique.")
        return value


# 👩‍🎓 Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['enrollment_date']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Name should only contain letters and spaces.")
        return value

    def validate_age(self, value):
        if value < 18 or value > 60:
            raise serializers.ValidationError("Age must be between 18 and 60.")
        return value

    def validate_email(self, value):
        allowed_domains = ('.edu', '.ac.in', '.edu.in')
        if not value.endswith(allowed_domains):
            raise serializers.ValidationError("Email must end with .edu, .ac.in, or .edu.in.")
        return value

    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Phone number should contain only digits.")
            if len(value) != 10:
                raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value


# 🎯 Course Detail Serializer
class StudentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age']


class CourseDetailSerializer(serializers.ModelSerializer):
    students = StudentMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_code', 'students']


# 👤 User Serializer (New)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create and return a User instance (do not return a dict)
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        # Ensure a Token exists for the user (DRF Token Authentication)
        Token.objects.get_or_create(user=user)

        return user
