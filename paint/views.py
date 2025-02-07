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
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully...")
            if user.is_user:
                return redirect('user_dashboard')
            elif user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_worker:
                return redirect('worker_dashboard')
        else:
            messages.error(request, "Invalid email or password")
            print("Error Mesage")
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

@login_required
def admin_dashboard(request):
    if request.user.is_admin:    
        messages.info(request, f"Welcome admin")
    else:
        messages.info(request, f"You are not allowed to access this page ..")
        return redirect('signin')
    return render(request, 'admin_dashboard.html')



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
            return redirect('portfolio_lists')  # Redirect to a page that lists portfolios
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


def book_us(request):
    if request.method == "POST":
        service = request.POST['service']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        location = request.POST['location']
        message = request.POST['message']
        a = ContactRequest(name=name,address=address,email=email,location=location,service_type=service, message=message)
        a.save()
        messages.success(request, f"Your booking has been submited successfully, the team will reach out to you immediately")
        return redirect(request.META.get("HTTP_REFERER"))
    return render(request,'home.html')



def booking_requests(request):
    if not request.user.is_admin:
        messages.info(request, f"You are not authorized to access this page")
        return redirect("signin")
    bookings  = ContactRequest.objects.all()
    context = {'bookings':bookings}
    return render(request, 'bookings.html', context)



class UpdatePortfolio(LoginRequiredMixin,UpdateView):
    model = Portfolio
    template_name = 'update_portfolio.html'

    def get_context_data(request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'portfolios'
        context['list_name'] = 'portfolio_lists'
        return context
    
    
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your Portfolio has been updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("portfolio_detail", kwargs={"slug": self.request.user.user_id})



class PortfolioDeleteView(DeleteView, LoginRequiredMixin):
    model = Portfolio
    template_name = 'portfolio_confirm_delete.html'
    
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "portfolio_delete"
        
        return context
    
    def get_success_url(self):
        messages.success(self.request, f"Portfolio deleted successfully!")
        return reverse('portfolio_lists')
    

def portfolio_lists(request):
    portfolios = Portfolio.objects.all()
    context = {'portfolios':portfolios}
    return render(request, 'portfolio_lists', context)


class PortfolioDetailView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'portfolio_detail.html'
    context_object_name = 'portfolio'
    slug_field = 'portfolio_id'
    
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "portfolio_detail"
        return context


def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def worker_dashboard(request):
    return render(request, 'worker_dashboard.html')