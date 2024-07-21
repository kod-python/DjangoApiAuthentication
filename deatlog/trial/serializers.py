

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Authentic
from django.contrib.auth import authenticate
from .models import LoginUser

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Authentic
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        
    def validate_csrf_token(self, value):
        if value != 'expected_csrf_token': 
            raise serializers.ValidationError("Invalid CSRF token")
        return value
    
        
    def validate_email(self, value):
        if Authentic.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = LoginUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            authentic_user = Authentic.objects.get(email=email)
        except Authentic.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')

        if not authentic_user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')

        return data








class BatchLoginSerializer(serializers.Serializer):
    logins = LoginUserSerializer(many=True)
   

    def validate(self, data):
        logins = data.get('logins')
        results = []
        errors = []
        for login in logins:
            serializer = LoginUserSerializer(data=login)
            if serializer.is_valid():
                results.append({'email': login['email'], 'status': 'success'})
            else:
                errors.append({'email': login['email'], 'status': 'failure', 'errors': serializer.errors})

        if errors:
            raise serializers.ValidationError(errors)

        return {'results': results}






# class UserLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
    
#     class Meta:
#         model: Authentic
#         fields = ['id','email', 'password']
        
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         if email and password:
#             user = authenticate(email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError('Invalid email or password')
#         else:
#             raise serializers.ValidationError('Both email and password are required')

#         data['user'] = user
#         return data


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
    
#     def validate_csrf_token(self, value):
#         if value != 'expected_csrf_token': 
#             raise serializers.ValidationError("Invalid CSRF token")
#         return value
    
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         user = authenticate(email=email, password=password)
#         if user is None:
#             raise serializers.ValidationError("Invalid email or password")

#         return {'user': user}















