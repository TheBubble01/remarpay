from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    TechAdminOnlyView,
    CreateUserView,
    SuspendUserView,
    UserProfileView,
    ChangePasswordView,
    AssignRoleView,
    UserListView,
    ResetUserCredentialsView,
    UserPreferenceView,
)

urlpatterns = [
    # 🔐 Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 👤 User Management
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('suspend/', SuspendUserView.as_view(), name='suspend_user'),
    path('<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign_user_role'),
    path('<int:pk>/reset/', ResetUserCredentialsView.as_view(), name='reset_user_credentials'),
    path('list/', UserListView.as_view(), name='user_list'),

    # 👤 Profile & Preferences
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/preferences/', UserPreferenceView.as_view(), name='user_preference'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # 🛠️ Admin Dashboard
    path('tech-admin-dashboard/', TechAdminOnlyView.as_view(), name='tech_admin_dashboard'),
]
