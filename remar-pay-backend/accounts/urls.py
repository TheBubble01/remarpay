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
