from django.urls import path
from .views import *

app_name = 'communities'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:post_pk>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<int:post_pk>/update/', PostUpdateView.as_view(), name='update'),

]