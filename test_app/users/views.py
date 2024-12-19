from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView

from test_app.blog.forms import PostForm, CommentForm, PlantForm
from test_app.blog.models import Post, Comment, Plant, Category
from test_app.users.forms import EditProfileForm, ChangePasswordForm, UserRegistrationForm, ProfileForm, UserLoginForm
from test_app.users.models import Profile
from test_app.users.validators import staff_check, admin_check

class UserRegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        Profile.objects.create(user=user)
        messages.success(self.request, f"Registration successful! Welcome, {user.username}!")
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {user.username}!")
        else:
            messages.error(self.request, "Invalid login credentials.")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, FormView):
    template_name = 'users/edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        profile = Profile.objects.get(user=self.request.user)
        kwargs.update({
            'instance': profile,  # Pass the Profile instance
            'user': self.request.user,  # Pass the User object
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Ensure the user is available in the template
        return context


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('home')


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

    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})

@login_required
def profile_delete(request, pk):
    obj = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('profile_list')
    return render(request, 'users/private/profile_delete.html', {'object': obj})


#admin's crud - Post model
def post_list(request):
    posts = Post.objects.filter(is_deleted=False).order_by('-updated_at')
    return render(request, 'users/private/post_list.html', {'posts': posts})

@login_required
def post_edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk) if pk else None

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'users/private/edit_post.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'users/private/post_delete.html', {'post': post})

#admin's crud - Comment model
@user_passes_test(admin_check)
def comment_list(request):
    comments = Comment.objects.all().order_by('-created_at')
    context = {'comments': comments}
    return render(request, 'users/private/comment_list.html', context)


@user_passes_test(admin_check)
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('admin_comments')
    else:
        form = CommentForm(instance=comment)

    context = {'form': form, 'action': 'Edit'}
    return render(request, 'users/private/comment_edit.html', context)

@user_passes_test(admin_check)
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('admin_comments')

    context = {'comment': comment}
    return render(request, 'users/private/comment_delete.html', context)

#admin's crud - Plant model
@user_passes_test(admin_check)
def plants_list(request):
    plants = Plant.objects.all()
    return render(request, 'users/private/plants_list.html', {'plants': plants})

@user_passes_test(admin_check)
def plant_edit(request, pk):
    if pk == 0:
        plant = None
        form = PlantForm(request.POST or None, request.FILES or None)
    else:
        plant = get_object_or_404(Plant, pk=pk)
        form = PlantForm(request.POST or None, request.FILES or None, instance=plant)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('plants_list')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'users/private/plant_edit.html', {'form': form, 'plant': plant})

@user_passes_test(admin_check)
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants_list')

    return render(request, 'users/private/delete_plant.html', {'plant': plant})

#admin's crud - Category model
@user_passes_test(admin_check)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'users/private/category_list.html', {'categories': categories})
@user_passes_test(admin_check)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return redirect('category_list')
    return render(request, 'users/private/category_edit.html', {'category': category})

@user_passes_test(admin_check)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category_list')

    context = {'category': category}
    return render(request, 'users/private/category_delete.html', context)


@user_passes_test(staff_check)
def admin_dashboard(request):
    deleted_posts = Post.objects.filter(is_deleted=True).order_by('-updated_at')
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=thirty_days_ago).order_by('-last_login')

    latest_comments = Comment.objects.all().order_by('-created_at')[:5]

    posts_with_likes = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]

    context = {
        'deleted_posts': deleted_posts,
        'active_users': active_users,
        'latest_comments': latest_comments,
        'posts_with_likes': posts_with_likes,
    }

    return render(request, 'users/private/dashboard.html', context)

