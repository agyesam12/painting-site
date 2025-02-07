from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.detail import DetailView , BaseDetailView
from django.views.generic import TemplateView, View, UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth import login, logout, authenticate  
from django.utils.encoding import force_bytes, force_str   
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode  
from django.core.mail import EmailMessage, EmailMultiAlternatives 
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.utils.translation import activate
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.db import transaction
from django.http import JsonResponse
from django.utils.timezone import now,timedelta
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse,reverse_lazy
from django.views import View
from .models import *
from .forms import *
from .forms import UserRegistrationForm
#import stripe
from django.utils.decorators import method_decorator
from .forms import ServiceForm, PortfolioForm, TestimonialForm
#import stripe

# Create your views here.


def home(request):
    return render(request,'home.html')


def signin(request):
    return render(request, 'signin.html')

    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_user = True
            user.save()
            messages.success(request, f"Acount created successfully")
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
    


@login_required
def signout(request):
    logout(request)
    messages.success(request,f"You have logged out successfuly..")
    return redirect('signin')


def admin_dashboard(request):
    if not request.user.is_admin or request.user.is_staff:
        messages.info(request, f"You are not allowed to access this page")
        return redirect('signin')
    return render(request, 'user_dashboard.html')



@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            return redirect('service_list')  # Redirect to a page that lists services
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})


@login_required
def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.created_by = request.user
            portfolio.save()
            return redirect('portfolio_list')  # Redirect to a page that lists portfolios
    else:
        form = PortfolioForm()
    return render(request, 'create_portfolio.html', {'form': form})



@login_required
def create_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.save()
            return redirect('testimonial_list')  # Redirect to a page that lists testimonials
    else:
        form = TestimonialForm()
    return render(request, 'create_testimonial.html', {'form': form})