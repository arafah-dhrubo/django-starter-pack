from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from accounts.forms import CreateUserForm, LoginForm
from accounts.models import Profile
from accounts.forms import UpdateProfile, UpdateUser


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid:
                form.save()
                user = form.cleaned_data.get['username']
                messages.success(request, 'Congratulations ' + user + ' Account created successfully')
                return redirect("/")
        title = "Create Account"
        context = {
            'form': form,
            'title': title
        }
        return render(request, 'accounts/form.html', context)


def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'Already Logged In!')
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, request.user.username + ' Logged in Successfully')
                return redirect('/')
            else:
                messages.error(request, 'Wrong username or password')
                return redirect('login')
        title = "Login"
        context = {
            'title': title,
        }
        return render(request, 'accounts/login.html', context)


def logout_page(request):
    user=request.user.username
    logout(request)
    messages.success(request, user + ' Logged out Successfully')
    return redirect('/')

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        user_form = UpdateUser(request.POST, instance=request.user)
        profile_form = UpdateProfile(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            form = profile_form.save(commit=False)
            form.user = user_form
            form.save()
            messages.success(request, 'user profile has been updated')
            return redirect('/')
        else:
            messages.error(request, 'Form Submission Failed')
            return redirect('update_profile')
    else:
        user_form = UpdateUser(instance=request.user)
        profile_form = UpdateProfile(instance=profile)
        title = "Update Profile"
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': title
        }
        return render(request, 'accounts/update_profile.html', context)


def pass_change(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "your password has been updated")
            return redirect('profile')
    title = "Update Password"
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'accounts/form.html', context)
