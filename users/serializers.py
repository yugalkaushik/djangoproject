from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Invitation

class UserInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'uuid', 'email', 'is_used']
        
class RegisterUserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        # Validate uuid exists, not used, email matches
        try:
            invitation = Invitation.objects.get(uuid=data['uuid'], is_used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or used UUID.")

        if invitation.email != data['email']:
            raise serializers.ValidationError("Email mismatch for invitation.")
        return data

    def create(self, validated_data):
        invitation = Invitation.objects.get(uuid=validated_data['uuid'])
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        invitation.is_used = True
        invitation.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login with form-friendly field definitions.
    """
    username = serializers.CharField(
        max_length=150,
        help_text="Enter your username"
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Enter your password"
    )
