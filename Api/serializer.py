from rest_framework import serializers
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import *
from Usable import usable as uc
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fname', 'lname', 'email', 'password']

    def validate(self, data):
        requireFields = ['fname', 'lname', 'email', 'password']

        validator = uc.requireFeildValidation(data, requireFields)
        if not validator['status']:
            raise serializers.ValidationError({"error": validator["message"]})  # Change "requireFields" to "message"
        return data

    def validate_email(self, value):
        if not uc.checkemailforamt(value):
            raise serializers.ValidationError("Email Format Is Incorrect")
        return value


    def passwordLengthValidator(self, value):
        if not uc.validate_password(value):
            raise serializers.ValidationError("Password must contain at least one special character and one uppercase letter, and be between 8 and 20 characters long")
        return make_password(value)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        fetch_user = User.objects.filter(email=email).first()
        if not fetch_user:
            raise serializers.ValidationError("Email not found . . .")
        check_pass = handler.verify(password, fetch_user.password)
        if not check_pass:
            raise serializers.ValidationError("Wrong Password !!!")
        attrs["fetch_user"] = fetch_user
        return attrs



class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description"]

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['contributor_users']


class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"