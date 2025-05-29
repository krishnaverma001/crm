from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('customer/<int:k>', views.customer_view, name='customer'),
    path('delete/<int:k>', views.delete_customer, name='delete'),
    path('new/', views.new_customer, name='new'),
]