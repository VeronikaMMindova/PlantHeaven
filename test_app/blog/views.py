from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView

from test_app.blog.models import Post, Category, Plant, Comment
from test_app.blog.forms import PostForm, EditForm, CommentForm, CategoryForm


# class HomeView(ListView):
#     model = Post
#     template_name = '../templates/home/home.html'
#     categories_types = Category.objects.all()
#     ordering = ['-created_at']
#
#     def get_context_data(self, *args,**kwargs):
#         category_menu = Category.objects.all()
#         context = super(HomeView, self).get_context_data(*args,**kwargs)
#         context['category_menu'] = category_menu
#         return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user

        # Check if the user is authenticated and has a profile
        if user.is_authenticated and hasattr(user, 'profile'):
            profile = user.profile
            context['liked'] = post.likes.filter(id=profile.id).exists()
        else:
            context['liked'] = False

        # Add total likes to the context
        context['total_likes'] = post.total_likes()

        # Add the comments to the context
        context['comments'] = post.comments.all()

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        # Handle comment submission
        if request.method == 'POST' and request.user.is_authenticated:
            comment_text = request.POST.get('comment_text')
            if comment_text:
                # Create the comment and link it to the post
                Comment.objects.create(
                    post=post,
                    user=request.user.profile,  # Link to the user's profile
                    content=comment_text  # Save the comment text in the content field
                )
            # After posting a comment, redirect to the same post detail page
            return redirect('post_details', pk=post.pk)
        return super().post(request, *args, **kwargs)
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm  # Use the form you created for editing posts
    template_name = 'blog/update_post.html'
    context_object_name = 'post'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.author.user != self.request.user:
            raise PermissionDenied  # or redirect to some error page
        return post

    def form_valid(self, form):
        form.save()
        return redirect('post_details', pk=self.object.pk)



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
            # Handle unexpected cases or errors
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
        # Allow only staff or admin users
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_permissions(self):
        if self.request.user.is_authenticated:
            return super().get_permissions()
        else:
            return []


# function-based view
# def category_view(request, categories_types):
#     formatted_category = categories_types.replace('-', ' ').title()
#     category_post = Post.objects.filter(category__iexact=formatted_category)
#
#     # Debugging statement
#     # print(f"Formatted Category: {formatted_category}, Post Count: {category_post.count()}")
#
#
#
#     context = {
#         'categories_types': formatted_category,
#         'category_post': category_post,
#     }
#
#
#     return render(request, 'search_plants.html', context)
#
    # category_post = Post.objects.filter(category=categories_types.replace('-', ' '))
    # context = {'categories_types': categories_types.replace('-', ' '),'category_post': category_post}
    # return render(request, 'search_plants.html', context)
#
# def CategoryListView(request):
#     category_menu_list = Category.objects.all()
#     context = {'category_menu_list': category_menu_list}
#     return render(request, 'category_list.html', context)

# def LikeView(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     is_liked = False
#
#     # unlike
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         is_liked = False
#
#     # like
#     else:
#         post.likes.add(request.user)
#         is_liked = True
#
#
#     return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))
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

# def found_plant(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     plants = Plant.objects.filter(category=category)
#     return render(request, 'blog/plant_list.html', {'plants': plants, 'category': category})

# @login_required
# def confirm_delete_post(request,pk):
#     # Get the post to be deleted
#     post = get_object_or_404(Post, pk=pk)
#
#     # Ensure the logged-in user is the author of the post
#     if request.user != post.author.user:
#         raise Http404("You are not authorized to delete this post.")
#
#     # If the form is submitted via POST, perform soft delete
#     if request.method == "POST":
#         # Mark the post as deleted (soft delete)
#         post.is_deleted = True
#         post.save()
#
#         # Redirect to the home page after marking the post as deleted
#         return redirect('home')
#
#     return render(request, 'blog/confirm_delete_post.html', {'post': post})


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
