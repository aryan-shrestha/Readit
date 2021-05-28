from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('article/<str:slang>/', views.article, name='article'),
    path('category/<str:slang>/', views.category, name='category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('search/', views.search, name='search'),

    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<str:slang>/', views.update_post, name='update_post'),
    path('delete_post/<str:slang>/', views.delete_post, name='delete_post'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('comment/<int:pk>', views.add_comment, name='comment'),
    path('update_profile_pic/', views.update_profile_pic, name='update_profile_pic'),
    path('hit_like/<int:pk>', views.hit_like, name='hit_like'),
    path('hit_like/', views.like, name='hit_like'),

]