from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from .views import TechAdminOnlyView
urlpatterns += [
    path('tech-admin-dashboard/', TechAdminOnlyView.as_view(), name='tech_admin_dashboard'),
]

from .views import CreateUserView
urlpatterns += [
    path('register/', CreateUserView.as_view(), name='create_user'),
]

from .views import SuspendUserView

urlpatterns += [
    path('suspend/', SuspendUserView.as_view(), name='suspend_user'),
]

from .views import UserProfileView

urlpatterns += [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

from .views import ChangePasswordView

urlpatterns += [
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]

from .views import AssignRoleView

urlpatterns += [
    path('<int:pk>/assign-role/', AssignRoleView.as_view(), name='assign_user_role'),
]

from .views import UserListView

urlpatterns += [
    path('list/', UserListView.as_view(), name='user_list'),
]

from .views import ResetUserCredentialsView

urlpatterns += [
    path('<int:pk>/reset/', ResetUserCredentialsView.as_view(), name='reset_user_credentials'),
]

from .views import UserPreferenceView

urlpatterns += [
    path('profile/preferences/', UserPreferenceView.as_view(), name='user-preference'),
]
