from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Change to your home page URL name
        else:
            messages.error(request, 'Invalid email or password')
        
        return render(request, 'user/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return redirect('login')
    
    def post(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return redirect('login')


# Function-based views (alternative)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Change to your home page URL name
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')