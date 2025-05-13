from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model with role field for DaanSetu application
    """
    DONOR = 'donor'
    VOLUNTEER = 'volunteer'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (DONOR, 'Donor'),
        (VOLUNTEER, 'Volunteer'),
        (ADMIN, 'Admin'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=DONOR,
        verbose_name=_('Role')
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_donor(self):
        return self.role == self.DONOR
    
    @property
    def is_volunteer(self):
        return self.role == self.VOLUNTEER
    
    @property
    def is_admin_role(self):
        return self.role == self.ADMIN


class ItemDonation(models.Model):
    """
    Model for item donations
    """
    PENDING = 'pending'
    ASSIGNED = 'assigned'
    DELIVERED = 'delivered'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ASSIGNED, 'Assigned'),
        (DELIVERED, 'Delivered'),
    ]
    
    CONDITION_NEW = 'new'
    CONDITION_LIKE_NEW = 'like_new'
    CONDITION_GOOD = 'good'
    CONDITION_FAIR = 'fair'
    CONDITION_POOR = 'poor'
    
    CONDITION_CHOICES = [
        (CONDITION_NEW, 'New'),
        (CONDITION_LIKE_NEW, 'Like New'),
        (CONDITION_GOOD, 'Good'),
        (CONDITION_FAIR, 'Fair'),
        (CONDITION_POOR, 'Poor'),
    ]
    
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default=CONDITION_GOOD)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_donations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    pickup_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_name} by {self.donor.username}"
    
    class Meta:
        ordering = ['-created_at']


class MoneyDonation(models.Model):
    """
    Model for money donations
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='money_donations')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"₹{self.amount} by {self.donor.username}"
    
    class Meta:
        ordering = ['-date']


class VolunteerAssignment(models.Model):
    """
    Model for volunteer assignments to item donations
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    item = models.ForeignKey(ItemDonation, on_delete=models.CASCADE, related_name='assignments')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.volunteer.username} assigned to {self.item.item_name}"
    
    class Meta:
        ordering = ['-assigned_at']
        unique_together = ['volunteer', 'item']
