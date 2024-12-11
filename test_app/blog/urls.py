from django.urls import path


from test_app.blog.views import PostDetailView, AddPostView, DeletePostView, UpdatePostView, \
    AddCategoryView,  about_us_view, our_blog_view, like_post, search_plants, add_comment, \
    plant_list
from test_app.common.views import plants_by_category

urlpatterns = [
    # public part
    path('our_blog/', our_blog_view, name='our_blog'),
    path('about_us/', about_us_view, name='about_us'),
    path('search_plants/', search_plants, name='search_plants'),
    path('plants/', plant_list, name='plants'),
    path('plants/category/<str:category_name>/', plants_by_category, name='category_plants'),
    path('post/details/<int:pk>/', PostDetailView.as_view(), name='post_details'),
    # private part
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='confirm_delete_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    # path('post/<int:post_id>/delete_confirm/', confirm_delete_post, name='confirm_delete_post'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
]