from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.ModelSerializer):
    # Confirm password field (optional, for UX)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        # Create user using the manager
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'profile_pic', 'created_at']
        read_only_fields = ['email', 'role', 'created_at']  # Prevent editing these fields

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        # Check current password is correct
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError({"current_password": "Incorrect current password."})

        # Check new and confirm match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})

        # Optional: enforce strong password policy
        validate_password(data['new_password'], user)

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class AssignRoleSerializer(serializers.ModelSerializer):
    assigned_country = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['role', 'assigned_country']

    def validate(self, data):
        role = data.get('role')
        country = data.get('assigned_country')

        if role == 'agent' and not country:
            raise serializers.ValidationError("Assigned country is required for agents.")
        if role != 'agent':
            data['assigned_country'] = None
        return data

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.role == 'tech-admin':
            return None  # Skip tech-admins entirely
        return rep

class ResetUserCredentialsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        if not data.get('email') and not data.get('password'):
            raise serializers.ValidationError("Provide at least email or password to reset.")
        return data

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

# User timezone preference
class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['current_country', 'timezone', 'dark_mode']
