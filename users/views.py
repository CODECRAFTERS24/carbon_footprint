from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import TransportTicket, Voucher, UserProfile, UserVoucherRedemption
from .forms import TransportTicketForm
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('user_dashboard'))
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

from django.views.decorators.http import require_GET

@require_GET
def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_dashboard(request):
    """Render user dashboard with transport history and vouchers"""
    user_profile = UserProfile.objects.get(user=request.user)
    transport_tickets = TransportTicket.objects.filter(
        user=request.user
    ).order_by('-created_at')

    available_vouchers = Voucher.objects.filter(
        is_active=True, 
        points_required__lte=user_profile.reward_points,
        valid_until__gt=timezone.now()
    )

    context = {
        'transport_tickets': transport_tickets,
        'available_vouchers': available_vouchers,
        'user_profile': user_profile
    }

    return render(request, 'dashboard.html', context)

@login_required
def upload_ticket(request):
    """View to handle ticket uploads"""
    if request.method == 'POST':
        form = TransportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.co2_saved = form.calculate_co2_saved()
            ticket.save()

            # Update user profile
            profile = UserProfile.objects.get(user=request.user)
            profile.total_co2_saved += ticket.co2_saved
            profile.reward_points = int(profile.total_co2_saved * 10)  # 10 points per kg CO2
            profile.save()

            messages.success(request, f'Ticket uploaded successfully! {ticket.co2_saved:.2f} kg CO2 saved.')
            return redirect('user_dashboard')
    else:
        form = TransportTicketForm()
    
    return render(request, 'upload_ticket.html', {'form': form})

@login_required
def redeem_voucher(request, voucher_id):
    """Handle voucher redemption"""
    voucher = get_object_or_404(Voucher, id=voucher_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.reward_points >= voucher.points_required:
        # Deduct points and record redemption
        user_profile.reward_points -= voucher.points_required
        user_profile.save()

        # Record voucher redemption
        UserVoucherRedemption.objects.create(
            user=request.user, 
            voucher=voucher
        )

        messages.success(request, f'Voucher {voucher.name} redeemed successfully!')
    else:
        messages.error(request, 'Insufficient reward points.')

    return redirect('user_dashboard')