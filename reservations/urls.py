from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_reservation, name='book'),
    path('contact/', views.submit_contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/status/<int:reservation_id>/', views.dashboard_update_status, name='dashboard-status'),
    path('dashboard/toggle/<int:item_id>/', views.dashboard_toggle_menu, name='dashboard-toggle'),
]
