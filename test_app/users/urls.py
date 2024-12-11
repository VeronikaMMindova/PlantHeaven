from django.urls import path

from test_app.users.views import UserLoginView, UserRegistrationView, UserUpdateView, ChangePasswordView, \
    password_success, logout_view, admin_dashboard, profile_details

urlpatterns = [
    # private part
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', UserUpdateView.as_view(), name='edit_profile' ),
    path('<int:pk>/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('password_changed/', password_success, name='password_changed'),
    path('profile_details/', profile_details, name='profile_details'),
]