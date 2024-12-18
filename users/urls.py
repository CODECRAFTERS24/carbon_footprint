from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication Routes
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and Ticket Routes
    
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('upload-ticket/', views.upload_ticket, name='upload_ticket'),
    path('redeem-voucher/<int:voucher_id>/', views.redeem_voucher, name='redeem_voucher'),
]