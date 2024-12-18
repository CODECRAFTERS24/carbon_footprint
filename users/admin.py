from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, TransportTicket, Voucher, UserVoucherRedemption

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

class TransportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'transport_type', 'distance_traveled', 'co2_saved', 'verified', 'created_at')
    list_filter = ('transport_type', 'verified', 'created_at')
    search_fields = ('user__username', 'transport_type')

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'discount_percentage', 'valid_until', 'is_active')
    list_filter = ('is_active', 'valid_until')

class UserVoucherRedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'voucher', 'redeemed_at')
    list_filter = ('redeemed_at',)
    search_fields = ('user__username', 'voucher__name')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(TransportTicket, TransportTicketAdmin)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(UserVoucherRedemption, UserVoucherRedemptionAdmin)