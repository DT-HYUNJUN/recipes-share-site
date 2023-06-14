from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('recipes/', include('recipes.urls')),
    path('communities/', include('communities.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
