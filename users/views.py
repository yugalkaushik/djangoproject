from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Invitation
from .serializers import UserInviteSerializer, RegisterUserSerializer, LoginSerializer
from django.core.mail import send_mail

# Admin adds user + send invite email
class AdminAddUserView(generics.CreateAPIView):
    serializer_class = UserInviteSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        invite_url = f"http://127.0.0.1:8000/api/users/register/{instance.uuid}/"
        send_mail(
            "Your Registration Invite",
            f"Visit this link to register: {invite_url}",
            "from@example.com",
            [instance.email],
            fail_silently=False,
        )

# User registers via invite
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, uuid=None):
        data = request.data.copy()
        data['uuid'] = uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"status": "registered"}, status=status.HTTP_201_CREATED)

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
        
        # Get user by username and check password
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return Response({"status": "login success!", "username": username})
            else:
                return Response({"error": "Invalid credentials"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)
