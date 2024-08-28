from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_cv, name='upload_cv'),
    path("admin/", admin.site.urls)
]
