from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import User
from .permissions import IsTechAdmin, IsManager
from .serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer,
    AssignRoleSerializer,
    UserListSerializer,
    ResetUserCredentialsSerializer,
    UserPreferenceSerializer
)

# Force JWT for login to accept email for login instead of username
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# --------------------------------------------
# ✅ Tech Admin Dashboard
# --------------------------------------------
class TechAdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin]

    def get(self, request):
        return Response({"message": "Welcome, Tech Admin!"})


# --------------------------------------------
# ✅ User Creation (Tech Admin Only)
# --------------------------------------------
class CreateUserView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------------------------
# ✅ Suspend/Unsuspend User (Tech Admin & Manager)
# --------------------------------------------
class SuspendUserView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin | IsManager]

    def post(self, request):
        email = request.data.get('email')
        action = request.data.get('action')  # 'suspend' or 'unsuspend'

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if user.role == 'tech-admin':
            return Response({"error": "You cannot suspend a tech-admin."}, status=403)

        if action == 'suspend':
            user.is_active = False
        elif action == 'unsuspend':
            user.is_active = True
        else:
            return Response({"error": "Invalid action. Use 'suspend' or 'unsuspend'."}, status=400)

        user.save()
        return Response({
            "message": f"User {action}ed successfully.",
            "user": {
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active
            }
        }, status=200)


# --------------------------------------------
# ✅ Profile View/Update (All Users)
# --------------------------------------------
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "profile": serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)


# --------------------------------------------
# ✅ Change Password
# --------------------------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."})
        return Response(serializer.errors, status=400)


# --------------------------------------------
# ✅ Role Assignment (Tech Admin or Manager)
# --------------------------------------------
class IsManagerOrTechAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['manager', 'tech-admin']

class AssignRoleView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AssignRoleSerializer
    permission_classes = [IsManagerOrTechAdmin]
    http_method_names = ['patch']


# --------------------------------------------
# ✅ Reset Credentials (Tech Admin Only)
# --------------------------------------------
class ResetUserCredentialsView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetUserCredentialsSerializer
    permission_classes = [IsTechAdmin]
    http_method_names = ['patch']


# --------------------------------------------
# ✅ User List (Excludes Tech Admins)
# --------------------------------------------
class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(role='tech-admin')


# --------------------------------------------
# ✅ User Preferences (Country, Timezone, Theme)
# --------------------------------------------
class UserPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserPreferenceSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserPreferenceSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Preferences updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=400)
