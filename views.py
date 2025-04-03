from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DoctorProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account has been created! You can now complete your profile.')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        d_form = None
        
        if request.user.user_type == 'doctor':
            d_form = DoctorProfileForm(request.POST, instance=request.user)
            forms_valid = u_form.is_valid() and p_form.is_valid() and d_form.is_valid()
        else:
            forms_valid = u_form.is_valid() and p_form.is_valid()
        
        if forms_valid:
            u_form.save()
            p_form.save()
            if d_form:
                d_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
        d_form = DoctorProfileForm(instance=request.user) if request.user.user_type == 'doctor' else None
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'd_form': d_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def doctor_list(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'users/doctor_list.html', {'doctors': doctors}) 