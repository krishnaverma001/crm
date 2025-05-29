from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .forms import CustomerForm
from .models import Customer


def index_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('index')

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'index.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another one.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('signup')

        if password1 != password2:
            messages.error(request, 'Passwords do not match. Please re-enter.')
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, 'Username should contain only letters and numbers.')
            return redirect('signup')

        try:
            validate_password(password1)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect('signup')

        new_user = User.objects.create_user(username=username, email=email, password=password1)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        messages.success(request, "Your account was successfully created. Please login.")
        return redirect('index')

    return render(request, 'signup.html')


def dashboard_view(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        if not customers:
            messages.error(request, 'No customers added')

        return render(request, 'dashboard.html', {'customers': customers})
    else:
        messages.error(request, 'You must be Logged In')
        return redirect('index')

def customer_view(request, k):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=k)
        return render(request, 'record.html', {'record': customer})
    else:
        messages.error(request, 'You must be Logged In')
        return redirect('index')

def new_customer(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be Logged In')
        return redirect('index')

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully")
            return redirect('dashboard')  # Or wherever you want to go
        else:
            messages.error(request, "Invalid response")
    else:
        form = CustomerForm()

    return render(request, 'new.html', {'form': form})

def delete_customer(request, k):
    if request.user.is_authenticated:
        x = Customer.objects.get(id=k)
        x.delete()
        messages.success(request, 'Customer removed')
        return redirect('dashboard')
    else:
        messages.error(request, 'You must be Logged In')
        return redirect('index')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect("index")
