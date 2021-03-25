from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('find/', views.find, name='find'),
    path('create/', views.create, name='create'),
    path('register/', views.register, name='register'),

    path('api/', include('api_musifetch.urls')),
]
