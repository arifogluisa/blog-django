from django.urls import path
from .views import (BaseIndexView, BlogDetailView, BlogCreateView,
                    post_like, BlogCategoryView, AboutView,
                    ContactView, SearchView, MyBlogsView,
                    ManifestView, PushwooshServiceWorkerView,)


urlpatterns = [
    path('', BaseIndexView.as_view(), name='index'),
    path('blogs/', MyBlogsView.as_view(), name='my-blogs'),
    path('blogs/<slug:slug>', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/new/', BlogCreateView.as_view(), name='blog-create'),
    path('like/<int:pk>', post_like, name='blog_like'),
    path('categories/<slug:slug>', BlogCategoryView.as_view(), name='blog-by-category'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('search/', SearchView.as_view(), name='search'),
    path('manifest.json/', ManifestView.as_view(content_type="application/json"), name='manifest'),
    path('pushwoosh-service-worker.js/', PushwooshServiceWorkerView.as_view(
        content_type="application/x-javascript"), name='ps-worker'),
]
