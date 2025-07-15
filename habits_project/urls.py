from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habits.urls')),
    path('login/',  auth_views.LoginView.as_view(
                         template_name='login.html',
                         redirect_authenticated_user=True,
                     ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
