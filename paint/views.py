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
from .models import BOOKING_SERVICE_TYPE
from .forms import *
from .forms import UserRegistrationForm
#import stripe
from django.utils.decorators import method_decorator
from .forms import ServiceForm, PortfolioForm, TestimonialForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
#import stripe

# Create your views here.


def home(request):
    if request.method == "POST":
        service = request.POST['service']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        location = request.POST['location']
        phone =request.POST['phone']
        message = request.POST['message']
        a = ContactRequest(name=name,address=address,email=email,location=location,service_type=service,phone=phone, message=message)
        a.save()
        messages.success(request, f"Your booking has been submited successfully, the team will reach out to you immediately")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        context = {
            'booking_service_types': BOOKING_SERVICE_TYPE
        }
        print("Form not submitted yet")
    return render(request,'home.html',context)


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
        total_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
        pending_bookings = ContactRequest.objects.filter(service_type__in=[service[0] for service in BOOKING_SERVICE_TYPE])
        portfolio_updates = Portfolio.objects.all().order_by('-created_at')[:10]  # Fetch the latest 10 portfolio updates
        context = {
            'total_notifications': total_notifications,
            'pending_bookings': pending_bookings,
            'portfolio_updates': portfolio_updates,
        }
    else:
        messages.info(request, f"You are not allowed to access this page ..")
        return redirect('signin')
    return render(request, 'admin_dashboard.html',context)



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
        name = request.POST['name']
        service = request.POST['service']
        address = request.POST['address']
        email = request.POST['email']
        location = request.POST['location']
        phone =request.POST['phone']
        message = request.POST['message']
        
        # Create and save the contact request
        a = ContactRequest(name=name, address=address, email=email, location=location, service_type=service,phone=phone, message=message)
        a.save()
        
        messages.success(request, "Your booking has been submitted successfully. The team will reach out to you immediately.")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        context = {
            'booking_service_types': BOOKING_SERVICE_TYPE
        }
        print("Form not submitted yet")
    return render(request, 'book_us.html',context)



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
    fields =['title','description','before_image','after_image']

    def get_context_data(request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'portfolios'
        context['list_name'] = 'portfolio_lists'
        return context
    
    def get_object(self, queryset=None):
        return Portfolio.objects.get(portfolio_id=self.kwargs['portfolio_id'])

    
    def form_valid(self, form):
        messages.success(self.request, 'Your Portfolio has been updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("portfolio_detail", kwargs={"pk": self.object.pk})



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
    return render(request, 'portfolio_lists.html', context)


class PortfolioDetailView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'portfolio_detail.html'
    context_object_name = 'portfolio'
    slug_field = 'portfolio_id'

    def get_object(self, queryset=None):
        return Portfolio.objects.get(portfolio_id=self.kwargs['portfolio_id'])
    
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "portfolio_detail"
        return context


def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def worker_dashboard(request):
    return render(request, 'worker_dashboard.html')


class DisplayNotifications(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'notifications'
        context['list_name'] = 'notifications'
        return context


    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user,created_at__lt=timezone.now(),is_read=False).order_by('created_at')
    

def mark_notification_read(request, notification_id):
    if request.method == "POST":
        try:
            notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({"success": True})
        except Exception as e:
            print(f"Error marking notification as read: {e}")  # Debugging
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def display_notifications(request):
    notifications = Notification.objects.all()
    context = {'notifications':notifications}
    return render(request, 'all_notifications.html', context)


class DisplayPortfolios(ListView):
    model = Portfolio
    template_name = 'portfolio_lists.html'
    context_object_name = 'portfolios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'portfolios'
        context['list_name'] = 'portfolis'
        return context
    
    def get_queryset(self):
        return Portfolio.objects.filter(created_at__lt=timezone.now()).order_by('created_at')