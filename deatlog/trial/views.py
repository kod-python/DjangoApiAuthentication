
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
    # serializer_class = BatchLoginSerializer
    # permission_classes = [AllowAny]
    def post(self, request):
        serializer = BatchLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













