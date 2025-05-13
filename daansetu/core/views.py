from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import User, ItemDonation, MoneyDonation, VolunteerAssignment
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    ItemDonationForm, MoneyDonationForm, VolunteerAssignmentForm
)
from .decorators import (
    donor_required, volunteer_required, admin_required, redirect_based_on_role
)

@redirect_based_on_role
def home(request):
    """
    Home page with statistics and information
    """
    # Get statistics for the home page
    item_count = ItemDonation.objects.count()
    money_sum = MoneyDonation.objects.aggregate(total=Sum('amount'))['total'] or 0
    volunteer_count = User.objects.filter(role=User.VOLUNTEER).count()
    donor_count = User.objects.filter(role=User.DONOR).count()
    
    context = {
        'item_count': item_count,
        'money_sum': money_sum,
        'volunteer_count': volunteer_count,
        'donor_count': donor_count,
    }
    return render(request, 'home.html', context)

@redirect_based_on_role
def register(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)
            messages.success(request, 'Registration successful!')
            
            # Redirect based on role
            if user.is_donor:
                return redirect('donor_dashboard')
            elif user.is_volunteer:
                return redirect('volunteer_dashboard')
            elif user.is_admin_role:
                return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@redirect_based_on_role
def login_view(request):
    """
    Custom login view to handle role-based redirection
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on role
                if user.is_donor:
                    return redirect('donor_dashboard')
                elif user.is_volunteer:
                    return redirect('volunteer_dashboard')
                elif user.is_admin_role:
                    return redirect('admin_dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# Donor Views
@login_required
@donor_required
def donor_dashboard(request):
    """
    Dashboard for donors
    """
    recent_items = ItemDonation.objects.filter(donor=request.user).order_by('-created_at')[:5]
    recent_money = MoneyDonation.objects.filter(donor=request.user).order_by('-date')[:5]
    
    item_count = ItemDonation.objects.filter(donor=request.user).count()
    money_sum = MoneyDonation.objects.filter(donor=request.user).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'recent_items': recent_items,
        'recent_money': recent_money,
        'item_count': item_count,
        'money_sum': money_sum,
    }
    return render(request, 'donor/dashboard.html', context)

@login_required
@donor_required
def donate_item(request):
    """
    View for donors to donate items
    """
    if request.method == 'POST':
        form = ItemDonationForm(request.POST)
        if form.is_valid():
            item_donation = form.save(commit=False)
            item_donation.donor = request.user
            item_donation.save()
            messages.success(request, 'Item donation submitted successfully!')
            return redirect('donor_dashboard')
    else:
        form = ItemDonationForm()
    
    return render(request, 'donor/donate_item.html', {'form': form})

@login_required
@donor_required
def donate_money(request):
    """
    View for donors to donate money
    """
    if request.method == 'POST':
        form = MoneyDonationForm(request.POST)
        if form.is_valid():
            money_donation = form.save(commit=False)
            money_donation.donor = request.user
            money_donation.save()
            messages.success(request, 'Money donation submitted successfully!')
            return redirect('donor_dashboard')
    else:
        form = MoneyDonationForm()
    
    return render(request, 'donor/donate_money.html', {'form': form})

@login_required
@donor_required
def donation_history(request):
    """
    View for donors to see their donation history
    """
    item_donations = ItemDonation.objects.filter(donor=request.user).order_by('-created_at')
    money_donations = MoneyDonation.objects.filter(donor=request.user).order_by('-date')
    
    context = {
        'item_donations': item_donations,
        'money_donations': money_donations,
    }
    return render(request, 'donor/history.html', context)

# Volunteer Views
@login_required
@volunteer_required
def volunteer_dashboard(request):
    """
    Dashboard for volunteers
    """
    # Get unassigned donations
    unassigned_donations = ItemDonation.objects.filter(status=ItemDonation.PENDING)
    
    # Get assigned tasks for this volunteer
    assigned_tasks = VolunteerAssignment.objects.filter(
        volunteer=request.user
    ).select_related('item')
    
    pending_count = assigned_tasks.filter(status=VolunteerAssignment.PENDING).count()
    in_progress_count = assigned_tasks.filter(status=VolunteerAssignment.IN_PROGRESS).count()
    completed_count = assigned_tasks.filter(status=VolunteerAssignment.COMPLETED).count()
    
    context = {
        'unassigned_donations': unassigned_donations,
        'assigned_tasks': assigned_tasks,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'volunteer/dashboard.html', context)

@login_required
@volunteer_required
def volunteer_tasks(request):
    """
    View for volunteers to see their assigned tasks
    """
    # Get assigned tasks for this volunteer
    assigned_tasks = VolunteerAssignment.objects.filter(
        volunteer=request.user
    ).select_related('item')
    
    context = {
        'assigned_tasks': assigned_tasks,
    }
    return render(request, 'volunteer/tasks.html', context)

@login_required
@volunteer_required
def accept_donation(request, donation_id):
    """
    View for volunteers to accept an unassigned donation
    """
    donation = get_object_or_404(ItemDonation, id=donation_id, status=ItemDonation.PENDING)
    
    # Create an assignment
    assignment = VolunteerAssignment(
        volunteer=request.user,
        item=donation,
        status=VolunteerAssignment.IN_PROGRESS
    )
    assignment.save()
    
    # Update the donation status
    donation.status = ItemDonation.ASSIGNED
    donation.save()
    
    messages.success(request, f'You have accepted the donation: {donation.item_name}')
    return redirect('volunteer_dashboard')

@login_required
@volunteer_required
def complete_task(request, assignment_id):
    """
    View for volunteers to mark a task as completed
    """
    assignment = get_object_or_404(
        VolunteerAssignment,
        id=assignment_id,
        volunteer=request.user,
        status=VolunteerAssignment.IN_PROGRESS
    )
    
    # Update assignment
    assignment.status = VolunteerAssignment.COMPLETED
    assignment.completed_at = timezone.now()
    assignment.save()
    
    # Update donation status
    donation = assignment.item
    donation.status = ItemDonation.DELIVERED
    donation.save()
    
    messages.success(request, f'Task marked as completed: {donation.item_name}')
    return redirect('volunteer_tasks')

# Admin Views
@login_required
@admin_required
def admin_dashboard(request):
    """
    Dashboard for administrators
    """
    # Get statistics
    total_users = User.objects.count()
    donor_count = User.objects.filter(role=User.DONOR).count()
    volunteer_count = User.objects.filter(role=User.VOLUNTEER).count()
    admin_count = User.objects.filter(role=User.ADMIN).count()
    
    item_count = ItemDonation.objects.count()
    money_sum = MoneyDonation.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    pending_donations = ItemDonation.objects.filter(status=ItemDonation.PENDING).count()
    assigned_donations = ItemDonation.objects.filter(status=ItemDonation.ASSIGNED).count()
    delivered_donations = ItemDonation.objects.filter(status=ItemDonation.DELIVERED).count()
    
    # Get recent activity
    recent_items = ItemDonation.objects.order_by('-created_at')[:5]
    recent_money = MoneyDonation.objects.order_by('-date')[:5]
    recent_assignments = VolunteerAssignment.objects.order_by('-assigned_at')[:5]
    
    context = {
        'total_users': total_users,
        'donor_count': donor_count,
        'volunteer_count': volunteer_count,
        'admin_count': admin_count,
        'item_count': item_count,
        'money_sum': money_sum,
        'pending_donations': pending_donations,
        'assigned_donations': assigned_donations,
        'delivered_donations': delivered_donations,
        'recent_items': recent_items,
        'recent_money': recent_money,
        'recent_assignments': recent_assignments,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@admin_required
def admin_users(request):
    """
    View for administrators to manage users
    """
    donors = User.objects.filter(role=User.DONOR)
    volunteers = User.objects.filter(role=User.VOLUNTEER)
    admins = User.objects.filter(role=User.ADMIN)
    
    context = {
        'donors': donors,
        'volunteers': volunteers,
        'admins': admins,
    }
    return render(request, 'admin/users.html', context)

@login_required
@admin_required
def admin_donations(request):
    """
    View for administrators to manage donations
    """
    item_donations = ItemDonation.objects.all().order_by('-created_at')
    money_donations = MoneyDonation.objects.all().order_by('-date')
    
    context = {
        'item_donations': item_donations,
        'money_donations': money_donations,
    }
    return render(request, 'admin/donations.html', context)

@login_required
@admin_required
def assign_volunteer(request):
    """
    View for administrators to assign volunteers to donations
    """
    if request.method == 'POST':
        form = VolunteerAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.status = VolunteerAssignment.IN_PROGRESS
            assignment.save()
            
            # Update donation status
            donation = assignment.item
            donation.status = ItemDonation.ASSIGNED
            donation.save()
            
            messages.success(request, 'Volunteer assigned successfully!')
            return redirect('admin_dashboard')
    else:
        form = VolunteerAssignmentForm()
    
    return render(request, 'admin/assign_volunteer.html', {'form': form})

def logout_view(request):
    """
    Logout view that supports both GET and POST methods
    and redirects to the home page after logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
