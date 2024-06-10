# mysite/urls.py
from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('', views.landing, name='landing'),  # Set the landing page as the default
]
