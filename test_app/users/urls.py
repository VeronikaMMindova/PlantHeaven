from django.urls import path

from test_app.blog.views import plant_list
from test_app.users.views import UserLoginView, UserRegistrationView, UserUpdateView, ChangePasswordView, \
    password_success, logout_view, admin_dashboard, profile_details, superuser_dashboard, profile_list, profile_edit, \
    profile_delete, post_list, post_edit, post_delete, comment_list, comment_create, comment_edit, comment_delete, \
    plant_delete, plant_edit, category_edit, category_delete, plants_list, category_list

urlpatterns = [
    # private part
    path('admin/dashboard/',superuser_dashboard, name='superuser_dashboard'),

    # admin's crud on profile model
    path('admin/profiles/', profile_list, name='profile_list'),
    path('admin/profiles/edit/<int:pk>/', profile_edit, name='profile_edit'),
    path('admin/profiles/delete/<int:pk>/', profile_delete, name='profile_delete'),

    #admin's crud on post model
    path('admin/posts/', post_list, name='post_list'),
    path('admin/posts/edit/<int:pk>/', post_edit, name='post_edit'),
    path('admin/posts/delete/<int:pk>/', post_delete, name='post_delete_by_admin'),
    #
    # #admin's crud on comment model
    path('admin/comments/', comment_list, name='admin_comments'),
    path('admin/comments/create/',comment_create, name='comment_create'),
    path('admin/comments/edit/<int:pk>/', comment_edit, name='comment_edit'),
    path('admin/comments/delete/<int:pk>/', comment_delete, name='comment_delete'),

    #admin's crud on plants model
    path('admin/plants/', plants_list, name='plants_list'),
    path('admin/plants/edit/<int:pk>/', plant_edit, name='plant_edit'),
    path('admin/plants/delete/<int:pk>/', plant_delete, name='plant_delete'),

    #admin's crud on categories model
    path('admin/categories/', category_list, name='category_list'),
    path('admin/categories/edit/<int:pk>/', category_edit, name='category_edit'),
    path('admin/categories/delete/<int:pk>/', category_delete, name='category_delete'),



    path('dashboard/', admin_dashboard, name='dashboard'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', UserUpdateView.as_view(), name='edit_profile' ),
    path('<int:pk>/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('password_changed/', password_success, name='password_changed'),
    path('profile_details/', profile_details, name='profile_details'),

]