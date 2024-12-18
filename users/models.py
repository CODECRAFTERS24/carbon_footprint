from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Extended user profile to track reward points and carbon savings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_co2_saved = models.FloatField(default=0)
    reward_points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance)

class TransportTicket(models.Model):
    """Model to track individual transport tickets and carbon savings"""
    TRANSPORT_CHOICES = [
        ('bus', 'Bus'),
        ('metro', 'Metro'),
        ('train', 'Train'),
        ('tram', 'Tram'),
        ('bicycle', 'Bicycle')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_type = models.CharField(max_length=50, choices=TRANSPORT_CHOICES)
    distance_traveled = models.FloatField(help_text="Distance traveled in kilometers")
    ticket_image = models.ImageField(
        upload_to='tickets/', 
        validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])],
        help_text="Upload your ticket or proof of travel"
    )
    co2_saved = models.FloatField(default=0)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        related_name='verified_tickets', 
        on_delete=models.SET_NULL
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.transport_type} ticket on {self.created_at.date()}"

class Voucher(models.Model):
    """Vouchers that can be redeemed with reward points"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()
    discount_percentage = models.FloatField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserVoucherRedemption(models.Model):
    """Track voucher redemptions by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} redeemed {self.voucher.name}"