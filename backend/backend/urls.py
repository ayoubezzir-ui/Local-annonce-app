from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import logout_view, DashboardView, ProfileView, UserCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('annonces/', include('annonces.urls')),
    path('messages/', include('messages_app.urls')),
    path('users/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('users/logout/', logout_view, name='logout'),
    path('users/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('users/profile/', ProfileView.as_view(), name='profile'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)