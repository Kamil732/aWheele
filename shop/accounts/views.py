from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate

from queryset_sequence import QuerySetSequence
from products.models import Car, Part, Motorcycle
from . import forms

class LoginView(generic.FormView):
    template_name = 'accounts/login.html'
    form_class = forms.AuthenticateForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        login(self.request, user)

        next = self.request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('/')

class RegisterView(generic.CreateView):
    template_name = 'accounts/register.html'
    form_class = forms.RegisterForm

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)

        login(self.request, user)

        next = self.request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('/')

class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class MyProducts(generic.ListView):
    template_name = 'accounts/my_products.html'
    context_object_name = 'products'

    def get_products(self, status):
        if status == 'active':
            cars = Car.objects.filter(seller=self.request.user)
            parts = Part.objects.filter(seller=self.request.user)
            motorcycles = Motorcycle.objects.filter(seller=self.request.user)
        elif status == 'pending':
            cars = Car.pending_objects.filter(seller=self.request.user)
            parts = Part.pending_objects.filter(seller=self.request.user)
            motorcycles = Motorcycle.pending_objects.filter(seller=self.request.user)

        cars = cars if cars.exists() else Car.objects.none()
        parts = parts if parts.exists() else Part.objects.none()
        motorcycles = motorcycles if motorcycles.exists() else Motorcycle.objects.none()

        order = f"{'-' if self.request.GET.get('reverse', 'True') == 'True' else ''}{self.request.GET.get('lookup', 'pub_date')}"

        return QuerySetSequence(cars, parts, motorcycles).prefetch_related('images').order_by(order)

    def get_queryset(self):
        status = self.kwargs.get('status')
        qs = self.get_products(status)

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(MyProducts, self).get_context_data(*args, **kwargs)

        context['active_products_count'] = self.get_products('active').count()
        context['pending_products_count'] = self.get_products('pending').count()

        return context

    def get(self, request, *args, **kwargs):
        status = self.kwargs.get('status')

        if not self.get_products('pending').count() and status == 'pending':
            return HttpResponseRedirect(reverse('accounts:my-products', kwargs={'status': 'active'}))
        return super(MyProducts, self).get(request, *args, **kwargs)