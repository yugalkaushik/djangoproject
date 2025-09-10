from django.urls import path
from .views import AdminAddUserView, RegisterUserView, LoginView

urlpatterns = [
    path('admin/users/', AdminAddUserView.as_view(), name='admin-add-user'),
    path('register/<uuid:uuid>/', RegisterUserView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(), name='login-user'),
]
