from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Invitation
from .serializers import UserInviteSerializer, RegisterUserSerializer, LoginSerializer
from django.core.mail import send_mail

@method_decorator(csrf_exempt, name='dispatch')
class AdminAddUserView(generics.CreateAPIView):
    serializer_class = UserInviteSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]      

    def perform_create(self, serializer):
        instance = serializer.save()
        invite_url = f"http://127.0.0.1:8000/api/register/{instance.uuid}/"
        send_mail(
            "Your Registration Invite",
            f"Visit this link to register: {invite_url}",
            "from@example.com",
            [instance.email],
            fail_silently=False,
        )

# User registers via invite
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, uuid=None):
        data = request.data.copy()
        data['uuid'] = uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"status": "registered"}, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.CreateAPIView):
    """
    API endpoint for user login.
    Using CreateAPIView to show form fields in browsable API.
    """
    serializer_class = LoginSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Handle login logic when form is submitted.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": "login success!", 
                    "username": username,
                    "token": token.key 
                })
            else:
                return Response({"error": "Invalid credentials"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)
