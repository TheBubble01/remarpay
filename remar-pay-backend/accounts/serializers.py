from rest_framework import serializers
from .models import User

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
