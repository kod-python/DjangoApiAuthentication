from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSignupSerializer
# from .serializers import UserLoginSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import LoginUserSerializer
from .serializers import  BatchLoginSerializer
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .serializers import ResetEmailSerializer
from .utils.email import send_reset_email
from .utils.email import send_reset_email, generate_reset_token, save_reset_token, verify_token
from .serializers import ResetEmailSerializer, ConfirmTokenSerializer
from .models import Authentic




# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]


class UserLoginView(generics.GenericAPIView):
     serializer_class = LoginUserSerializer
     permission_classes = [AllowAny]
    
     def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BatchUserLoginView(APIView):
 
    def post(self, request):
        serializer = BatchLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password has been reset'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestResetEmailView(generics.GenericAPIView):
    serializer_class = ResetEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        user = get_object_or_404(Authentic, email=email)
        token = generate_reset_token()
        save_reset_token(user, token)
        send_reset_email(email, token)
        
        return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)


class ConfirmResetView(generics.GenericAPIView):
    serializer_class = ConfirmTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        user = get_object_or_404(Authentic, reset_token=token)
        
        if not verify_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        user.save()
        
        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)









# class SendResetEmailView(generics.GenericAPIView):
#     serializer_class = ResetEmailSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         token = serializer.validated_data['token']
        
#         try:
#             send_reset_email(email, token)
#             return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class SendResetEmailView(generics.GenericAPIView):
#     serializer_class = ResetEmailSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         token = serializer.validated_data['token']
        
#         try:
#             send_reset_email(email, token)
#             return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



