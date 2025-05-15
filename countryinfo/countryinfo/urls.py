from django.contrib import admin
from django.urls import path, include  
from django.contrib.auth import views as auth_views
from countries.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/', redirect_field_name=None), name='logout'),
    path('', include('countries.urls')),
    path('register/', register_view, name='register'),
]