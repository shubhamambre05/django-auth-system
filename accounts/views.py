from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'accounts/home.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Password do not match.')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists.')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created succesfully. Please login.')
        return redirect('login')
    
    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'logged out successfully!')
    return redirect('login')



