
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Authentic
from django.contrib.auth import authenticate
from .models import LoginUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)







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
        
        
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise serializers.ValidationError("Email domain is not allowed. Please use an email from the allowed domains.")
    
        if Authentic.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    
    
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         raise serializers.ValidationError("Passwords do not match.")
    #     return data

    
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        user = Authentic.objects.create(**validated_data)

        verification_url = f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}/"
        try:
            send_mail(
                'Email Verification',
                f'Click the link to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")

        return user
  


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



class ResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ConfirmTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()







# class ResetEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     token = serializers.CharField()









class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentic
        fields = ['email']

    def validate_email(self, value):
        try:
            user = Authentic.objects.get(email=value)
        except Authentic.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        return value

    def save(self):
        email = self.validated_data['email']
        user = Authentic.objects.get(email=email)
        user.generate_reset_token()

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{user.reset_token}/"
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = Authentic
        fields = ['token', 'new_password']

    def validate(self, data):
        try:
            user = Authentic.objects.get(reset_token=data['token'])
        except Authentic.DoesNotExist:
            raise serializers.ValidationError('Invalid token')
        return data

    def save(self):
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']
        user = Authentic.objects.get(reset_token=token)
        self.validated_data['password'] = make_password(new_password)
        # user.set_password(new_password)
        user.clear_reset_token()
        user.save()
        
        #  new_password = validated_data.pop('password')
        # validated_data['password'] = make_password(password)
        # user = Authentic.objects.create(**validated_data)

















# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         try:
#             user = Authentic.objects.get(email=value)
#         except Authentic.DoesNotExist:
#             raise serializers.ValidationError('User with this email does not exist.')
#         return value

#     def save(self):
#         email = self.validated_data['email']
#         user = Authentic.objects.get(email=email)
#         reset_token = get_random_string(length=32)
#         user.reset_token = reset_token
#         user.save()

#         reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_token}/"
#         send_mail(
#             'Password Reset Request',
#             f'Click the link to reset your password: {reset_url}',
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#             fail_silently=False,
#         )

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     new_password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         try:
#             user = Authentic.objects.get(reset_token=data['token'])
#         except Authentic.DoesNotExist:
#             raise serializers.ValidationError('Invalid token')
#         return data

#     def save(self):
#         token = self.validated_data['token']
#         new_password = self.validated_data['new_password']
#         user = Authentic.objects.get(reset_token=token)
#         user.set_password(new_password)
#         user.reset_token = None
#         user.save()











