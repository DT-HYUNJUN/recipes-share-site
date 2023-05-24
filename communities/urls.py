from django.urls import path
from .views import *

app_name = 'communities'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete'),

]