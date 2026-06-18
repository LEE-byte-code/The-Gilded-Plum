from django.urls import path
from . import views

urlpatterns = [
    path('api/menu/', views.menu_list, name='api-menu'),
    path('api/gallery/', views.gallery_list, name='api-gallery'),
    path('api/chef-table/', views.chef_table_availability, name='api-chef-table'),
    path('api/time-slots/', views.time_slots, name='api-time-slots'),
    path('api/check-availability/', views.check_availability, name='api-check-availability'),
]
