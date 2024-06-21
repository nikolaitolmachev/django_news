from django.urls import path, re_path, include
from rest_framework import routers

from . import views
from .api import api


router = routers.SimpleRouter()
router.register(r'news', api.NewsViewSet, basename='api')

urlpatterns = [
    path('', views.NewsHome.as_view(), name='home'),
    path('about/', views.about, name='about'),

    path('addpage/', views.AddPage.as_view(), name='add_page'),

    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),

    path('category/<slug:cat_slug>/', views.NewsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.NewsTags.as_view(), name='tag'),

    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='update_page'),

    path('api/', include(router.urls)),

    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]