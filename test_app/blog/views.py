from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView

from test_app.blog.models import Post, Category, Plant, Comment
from test_app.blog.forms import PostForm, CommentForm, CategoryForm, PlantForm, EditForm


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user


        if user.is_authenticated and hasattr(user, 'profile'):
            profile = user.profile
            context['liked'] = post.likes.filter(id=profile.id).exists()
        else:
            context['liked'] = False


        context['total_likes'] = post.total_likes()


        context['comments'] = post.comments.all()

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()


        if request.method == 'POST' and request.user.is_authenticated:
            comment_text = request.POST.get('comment_text')
            if comment_text:
                Comment.objects.create(
                    post=post,
                    user=request.user.profile,
                    content=comment_text
                )

            return redirect('post_details', pk=post.pk)
        return super().post(request, *args, **kwargs)
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user.profile
        else:
            raise PermissionDenied("You must be logged in to create a post.")
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('our_blog')
    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.author.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        return post

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    # def get_object(self):
    #     post = get_object_or_404(Post, pk=self.kwargs['pk'])
    #     if post.author.user != self.request.user:
    #         raise PermissionDenied
    #     return post
    #
    # def form_valid(self, form):
    #     form.save()
    #     return redirect('post_details', pk=self.object.pk)






class DeletePostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.user != post.author.user:
            raise Http404("You are not authorized to delete this post.")

        return render(request, 'blog/confirm_delete_post.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.user != post.author.user:
            raise Http404("You are not authorized to delete this post.")

        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            post.is_deleted = True
            post.save()
            return redirect('home')
        elif confirm == 'no':
            return redirect('post_details', pk=post.pk)
        else:
            return render(request, 'blog/confirm_delete_post.html', {
                'post': post,
                'error': "Invalid choice. Please confirm your action.",
            })

# private
class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'users/private/add_category.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    # def get_permissions(self):
    #     if self.request.user.is_authenticated:
    #         return super().get_permissions()
    #     else:
    #         return []


# function-based view
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)


    return redirect(request.META.get('HTTP_REFERER', 'home'))
def about_us_view(request):
    context = {}
    return render(request, template_name='blog/about_us.html',context=context)

def our_blog_view(request):
    posts = Post.objects.filter(is_deleted=False).order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, 'blog/our_blog.html', context)

def search_plants(request):
    query = request.GET.get('q', '')
    plants = Plant.objects.filter(name__icontains=query) if query else []
    context = {
        'query': query,
        'plants': plants,
    }
    return render(request, 'blog/search_plants.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_details',pk=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})


def plant_list(request):
    plants = Plant.objects.all()
    return render(request, 'blog/plants.html', {'plants': plants})

# private part
@login_required
def add_plant(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to add plants.")

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            category_name = plant.category.name
            return redirect('category_plants', category_name=category_name)
    else:
        form = PlantForm()

    return render(request, 'users/private/add_plant.html', {'form': form})
@login_required
def delete_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if request.method == "POST":
        plant.delete()
        return redirect('home')

    return render(request, 'users/private/delete_plant.html', {'plant': plant})
