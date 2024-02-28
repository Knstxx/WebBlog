from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path('',
         views.IndexListView.as_view(),
         name='index'
         ),
    path('login_only/',
         views.simple_view
         ),
    path('profile/<slug:username>/',
         views.ProfileListView.as_view(),
         name='profile'),

    path('posts/create/',
         views.IndexListView.as_view(),
         name='create_post'
         ),
    path('posts/<int:post_id>/edit/',
         views.IndexListView.as_view(),
         name='edit_post'
         ),
    path('posts/<int:post_id>/delete/',
         views.IndexListView.as_view(),
         name='delete_post'
         ),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'
         ),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'
         ),

    path('posts/<int:post_id>/comment/',
         views.IndexListView.as_view(),
         name='add_comment'
         ),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.IndexListView.as_view(),
         name='edit_comment'
         ),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.IndexListView.as_view(),
         name='delete_comment'
         ),
]
