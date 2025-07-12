from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

# Force the JWT to acceept email for login instead of username
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add extra info
        token['name'] = user.name
        token['role'] = user.role
        return token

    def validate(self, attrs):
        print("Login payload received:", attrs) # Debug login credentials
        data = super().validate(attrs)
        # Add user info in response
        data['user'] = {
            "id": self.user.id,
            "name": self.user.name,
            "role": self.user.role,
            "email": self.user.email
        }
        return data

# ----------------------
# ✅ User Creation
# ----------------------
class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)

# ----------------------
# ✅ Profile View/Update
# ----------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'profile_pic', 'created_at']
        read_only_fields = ['email', 'role', 'created_at']

# ----------------------
# ✅ Password Change
# ----------------------
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError({"current_password": "Incorrect current password."})
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})
        validate_password(data['new_password'], user)
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

# ----------------------
# ✅ Role + Country Assignment (Manager & Tech Admin)
# ----------------------
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

# ----------------------
# ✅ User List View (excluding tech-admins)
# ----------------------
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']

    def to_representation(self, instance):
        if instance.role == 'tech-admin':
            return None
        return super().to_representation(instance)

# ----------------------
# ✅ Reset Email or Password (Tech Admin)
# ----------------------
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

# ----------------------
# ✅ User Preference (timezone, country, dark mode)
# ----------------------
class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['current_country', 'timezone', 'dark_mode']
