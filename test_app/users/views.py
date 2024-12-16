from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.views.generic import CreateView, UpdateView, DetailView

from test_app.blog.forms import PostForm
from test_app.blog.models import Post, Comment, Plant, Category
from test_app.users.forms import EditProfileForm, ChangePasswordForm, UserRegistrationForm, ProfileForm
from test_app.users.models import Profile
from test_app.users.validators import staff_check, admin_check


# Create your views here.
class UserRegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    #
    # def form_valid(self, form):
    #     # Save the user instance but do not commit yet
    #     user = form.save(commit=False)
    #
    #     # Optionally: add any custom logic here for profile or user settings
    #
    #     # Save the user object to the database
    #     user.save()
    #
    #     # Log in the user automatically after successful registration
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #
    #     if user is not None:
    #         login(self.request, user)
    #         messages.success(self.request, "Registration successful! You are now logged in.")
    #
    #     # Optionally redirect to another page, like profile page
    #     return redirect('home')  # Or replace 'home' with the actual URL name

    def form_invalid(self, form):
        messages.error(self.request, "There were errors in your registration. Please check your inputs.")
        return self.render_to_response({'form': form})

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('home')

# class UserUpdateView(UpdateView):
#     form_class = EditProfileForm
#     template_name = 'users/edit_profile.html'
#     success_url = reverse_lazy('home')
#
#     def get_object(self):
#         return self.request.user
class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        # Allow users to edit their profile, but restrict status fields to admin
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('password_changed_succesfully')

# TODO:MAKE SHOW PROFILE
# class ShowProfilePageView(DetailView):
#     model = Profile
#     template_name = 'users/profile_details.html'
#     context_object_name = 'profile'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile = get_object_or_404(Profile, user__id=self.kwargs['pk'])
#         context['profile'] = profile
#         return context
def password_success(request):
    context = {}
    return render(request, 'users/password_changed_succesfully.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_details(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'users/profile_details.html', {'profile': profile})

#admin's crud - Profile model
@login_required
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'users/private/profile_list.html', {'profiles': profiles})

@login_required
def profile_edit(request, pk=None):
    profile = get_object_or_404(Profile, pk=pk) if pk else None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/register.html', {'form': form, 'profile': profile})

@login_required
def profile_delete(request, pk):
    obj = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('profile_list')
    return render(request, 'users/private/profile_delete.html', {'object': obj})

#admin's crud - Post model
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'users/private/post_list.html', {'posts': posts})

# TODO: make it redirect to edt_post.html
# @login_required
# def post_edit(request, pk=None):
#     post = get_object_or_404(Post, pk=pk) if pk else None
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm(instance=post)
#
#     return render(request, 'crud/post_form.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    """
    View to handle the deletion of a post.
    """
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'crud/post_confirm_delete.html', {'post': post})
@user_passes_test(staff_check)
def admin_dashboard(request):
    deleted_posts = Post.objects.filter(is_deleted=True)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=thirty_days_ago)

    latest_comments = Comment.objects.all().order_by('-created_at')[:5]

    posts_with_likes = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]

    context = {
        'deleted_posts': deleted_posts,
        'active_users': active_users,
        'latest_comments': latest_comments,
        'posts_with_likes': posts_with_likes,
    }

    return render(request, 'users/private/dashboard.html', context)

@user_passes_test(admin_check)
def superuser_dashboard(request):
    deleted_posts = Post.objects.filter(is_deleted=True)
    thirty_days_ago = now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=thirty_days_ago)
    latest_comments = Comment.objects.all().order_by('-created_at')[:5]
    posts_with_likes = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]

    # Model Counts
    profiles_count = Profile.objects.count()
    posts_count = Post.objects.count()
    comments_count = Comment.objects.count()
    plants_count = Plant.objects.count()
    categories_count = Category.objects.count()

    context = {
        'deleted_posts': deleted_posts,
        'active_users': active_users,
        'latest_comments': latest_comments,
        'posts_with_likes': posts_with_likes,
        'profiles_count': profiles_count,
        'posts_count': posts_count,
        'comments_count': comments_count,
        'plants_count': plants_count,
        'categories_count': categories_count,
    }
    return render(request, 'users/private/superuser_dashboard.html', context)