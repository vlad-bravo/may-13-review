from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='list'),
    path('create/', views.create_review, name='create'),
    path('edit/<int:pk>/', views.edit_review, name='edit'),
    path('delete/<int:pk>/', views.delete_review, name='delete'),
    path('stats/', views.review_stats, name='stats'),
]
