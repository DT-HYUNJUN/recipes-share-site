from django.urls import path
from .views import *

app_name = 'communities'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:post_pk>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<int:post_pk>/update/', PostUpdateView.as_view(), name='update'),
    path('<int:post_pk>/like/', PostLikeView.as_view(), name='post_like'),

    # 코멘트
    path('<int:post_pk>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('<int:post_pk>/<int:comment_pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('<int:post_pk>/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]