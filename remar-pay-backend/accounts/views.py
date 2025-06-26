from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserCreateSerializer
from .permissions import IsTechAdmin, IsManager
from rest_framework.permissions import IsAuthenticated
from .models import User

# Only accessible by tech-admins
class TechAdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin]

    def get(self, request):
        return Response({"message": "Welcome, Tech Admin!"})

# View for tech-admin to create users
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

# View for suspending/unsuspending users
class SuspendUserView(APIView):
    permission_classes = [IsAuthenticated, IsTechAdmin | IsManager]

    def post(self, request):
        email = request.data.get('email')
        action = request.data.get('action')  # 'suspend' or 'unsuspend'

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        # Prevent self-suspension or suspending tech-admins
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
