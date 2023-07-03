import math
from statistics import mean

from django.shortcuts import render, reverse
from django.utils.translation import gettext_lazy as _
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, View, CreateView
from django.contrib import messages
from django.core.mail import send_mail
# from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from django_countries.data import COUNTRIES
from queryset_sequence import QuerySetSequence

from . import forms
from .models import Car, Part, Motorcycle, MARK, YEAR_PRODUCTION, FUEL_TYPE, COLOR, GEARBOX, PART_TYPE, MOTORCYCLE_TYPE, DRIVE, CAR_TYPE
from accounts.models import Account
from cities_light.models import City
from cities_light.loading import CITIES

class PromoListView(ListView):
    template_name = 'products/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        product_type = self.request.GET.get('product_type', '')

        if product_type == 'motorcycle':
            qs = Motorcycle.objects.select_related('city').prefetch_related('images').filter(promo_days__gte=timezone.localdate()).order_by('-pub_date')[:10]
        elif product_type == 'part':
            qs = Part.objects.select_related('city').prefetch_related('images').filter(promo_days__gte=timezone.localdate()).order_by('-pub_date')[:10]
        else:
            qs = Car.objects.select_related('city').prefetch_related('images').filter(promo_days__gte=timezone.localdate()).order_by('-pub_date')[:10]

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(PromoListView, self).get_context_data(*args, **kwargs)

        context['marks'] = MARK
        context['year_production'] = YEAR_PRODUCTION
        context['fuel_type'] = FUEL_TYPE
        context['part_type'] = PART_TYPE
        context['motorcycle_type'] = MOTORCYCLE_TYPE

        return context

class SearchProductView(ListView):
    template_name = 'products/search_product_list.html'
    paginate_by = 20
    context_object_name = 'products'

    def get_queryset(self):
        product_type = self.request.GET.get('product_type')
        if product_type is None:
            raise Http404

        condition = self.request.GET.get('condition')
        mark = self.request.GET.get('mark')
        from_price = self.request.GET.get('from_price')
        to_price = self.request.GET.get('to_price')
        location = self.request.GET.get('location')

        # Car and Motorcycle
        if product_type == 'car' or product_type == 'motorcycle':
            from_year_production = self.request.GET.get('from_year_production')
            to_year_production = self.request.GET.get('to_year_production')

            from_mileage = self.request.GET.get('from_mileage')
            to_mileage = self.request.GET.get('to_mileage')

            from_power = self.request.GET.get('from_power')
            to_power = self.request.GET.get('to_power')

            country_of_origin = self.request.GET.get('country_of_origin')
            color = self.request.GET.get('color')
            gearbox = self.request.GET.get('gearbox')
            first_owner = self.request.GET.get('first_owner')

            # Car
            if product_type == 'car':
                promo_qs = Car.objects.filter(promo_days__gte=timezone.localdate()).order_by('-pub_date').select_related('city').prefetch_related('images')
                rest_qs = Car.objects.filter(Q(promo_days__lt=timezone.localdate()) | Q(promo_days=None)).order_by('-pub_date').select_related('city').prefetch_related('images')
                qs = QuerySetSequence(promo_qs, rest_qs).select_related('city').prefetch_related('images')

                fuel_type = self.request.GET.get('fuel_type')
                drive = self.request.GET.get('drive')
                right_hand_drive = self.request.GET.get('right_hand_drive')
                car_type = self.request.GET.get('car_type')

                # # Filters (car)
                if fuel_type:
                    qs = qs.filter(fuel_type=fuel_type)
                if drive:
                    qs = qs.filter(drive=drive)
                if right_hand_drive == 'True':
                    qs = qs.filter(right_hand_drive=right_hand_drive)
                if car_type:
                    qs = qs.filter(car_type=car_type)

            # Motorcycle
            elif product_type == 'motorcycle':
                promo_qs = Motorcycle.objects.filter(promo_days__gte=timezone.localdate()).order_by('-pub_date').select_related('city').prefetch_related('images')
                rest_qs = Motorcycle.objects.filter(Q(promo_days__lt=timezone.localdate()) | Q(promo_days=None)).order_by('-pub_date').select_related('city').prefetch_related('images')
                qs = QuerySetSequence(promo_qs, rest_qs).select_related('city').prefetch_related('images')

                motorcycle_type = self.request.GET.get('motorcycle_type')

                # Filters (motorcycle)
                if motorcycle_type:
                    qs = qs.filter(motorcycle_type=motorcycle_type)

            # Filters (car and motorcycle)
            if from_year_production:
               qs = qs.filter(year_production__gte=from_year_production)
            if to_year_production:
                qs = qs.filter(year_production__lte=to_year_production)
            if from_mileage:
                qs = qs.filter(mileage__gte=from_mileage)
            if to_mileage:
                qs = qs.filter(mileage__lte=to_mileage)
            if from_power:
                qs = qs.filter(power__gte=from_power)
            if to_power:
                qs = qs.filter(power__lte=to_power)
            if country_of_origin:
                qs = qs.filter(country_of_origin=country_of_origin)
            if color:
                qs = qs.filter(color=color)
            if gearbox:
                qs = qs.filter(gearbox=gearbox)
            if first_owner:
                qs = qs.filter(first_owner=first_owner)

        # Part
        elif product_type == 'part':
            promo_qs = Part.objects.filter(promo_days__gte=timezone.localdate()).order_by('-pub_date').select_related('city').prefetch_related('images')
            rest_qs = Part.objects.filter(Q(promo_days__lt=timezone.localdate()) | Q(promo_days=None)).order_by('-pub_date').select_related('city').prefetch_related('images')
            qs = QuerySetSequence(promo_qs, rest_qs).select_related('city').prefetch_related('images')
            # qs = Part.objects.order_by('-promo_days', '-pub_date')

            part_type = self.request.GET.get('part_type')
            delivery = self.request.GET.get('delivery')

            # Filters (part)
            if part_type:
                qs = qs.filter(part_type=part_type)
            if delivery == True:
                qs = qs.filter(delivery=True)

        # Filters (main)
        if condition:
            qs = qs.filter(condition=condition)
        if mark:
            qs = qs.filter(mark=mark)
        if from_price:
            qs = qs.filter(price__gte=from_price)
        if to_price:
            qs = qs.filter(price__lte=to_price)
        if location:
            qs = qs.filter(city__slug=location)

        return qs.select_related('city').prefetch_related('images')

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)

        context['today'] = timezone.localdate()
        context['offers_count'] = self.get_queryset().count()

        context['marks'] = MARK
        context['year_production'] = YEAR_PRODUCTION
        context['fuel_type'] = FUEL_TYPE
        context['part_type'] = PART_TYPE
        context['motorcycle_type'] = MOTORCYCLE_TYPE
        context['countries'] = COUNTRIES
        context['colors'] = COLOR
        context['gearboxes'] = GEARBOX
        context['drives'] = DRIVE
        context['cities'] = CITIES
        context['car_types'] = CAR_TYPE

        return context

class GetCityLocation(View):
    @staticmethod
    def get_distance(x1, x2, y1, y2):
        φ1 = float(x1) * math.pi/180
        φ2 = float(x2) * math.pi/180
        Δφ = (float(x2) - float(x1)) * math.pi/180
        Δλ = (float(y2) - float(y1)) * math.pi/180

        a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return 6371e3 * c # 6371e3 is the radius of the Earth

    def get(self, request):
        if request.is_ajax():
            data = {}
            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')

            nearest_city = {}
            for city_latitude, city_longitude, id in City.objects.values_list('latitude', 'longitude', 'id'):
                dist = self.get_distance(city_latitude, latitude, city_longitude, longitude)

                if not nearest_city or dist < nearest_city['distance']:
                    nearest_city['id'] = id
                    nearest_city['distance'] = dist

            data['nearest_city'] = list(City.objects.filter(id=nearest_city['id']).values_list('slug', flat=True))
            return JsonResponse(data)
        raise Http404

import phonenumbers

class ShowPhonenumber(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}

            product_clas = globals()[self.kwargs.get('section').capitalize()]
            product_slug = self.kwargs.get('product_slug')
            product = product_clas.objects.get(slug=product_slug)

            data['phonenumber'] = phonenumbers.format_number(product.phonenumber, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            if not product.seller == request.user:
                product.phonenumber_views += 1
                product.save()

            return JsonResponse(data)
        raise Http404

class SendEmail(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}

            section = self.kwargs.get('section')
            product_slug = self.kwargs.get('product_slug')
            product_class = globals()[section.capitalize()]
            product = product_class.objects.get(slug=product_slug)

            email = request.POST.get('email')
            phonenumber = request.POST.get('phonenumber')
            message = 'Wiadomość klienta: \n \n' + request.POST.get('message')

            if phonenumber:
                message += f'\n \n Numer telefonu klienta: {phonenumber}'
            message += f'\n E-mail klienta: {email}'

            send_mail(f'Ktoś jest zainteresowany twoją ofertą "{product.get_title()}"', message, email, [product.email], fail_silently=False)
            data['message'] = _('Your message has been sent successfuly')
            return JsonResponse(data)
        raise Http404

class GetAveragePrice(View):
    def get(self, request, product_class):
        if request.is_ajax():
            data = {}

            if product_class.lower() == 'car':
                year_production = request.GET.get('year_production')
                mark = request.GET.get('mark')
                fuel_type = request.GET.get('fuel_type')
                power = int(request.GET.get('power'))
                num_of_doors = int(request.GET.get('num_of_doors'))
                gearbox = request.GET.get('gearbox')
                mileage = int(request.GET.get('mileage'))
                right_hand_drive = request.GET.get('right_hand_drive', False)

                similar_products = Car.objects.filter(pub_date__gte=timezone.now() - timezone.timedelta(days=365), mark=mark, gearbox=gearbox, mileage__range=(mileage-2000, mileage+2000), power=power, year_production=year_production, fuel_type=fuel_type, num_of_doors=num_of_doors, right_hand_drive=right_hand_drive)
                if similar_products.count() >= 8:
                    prices = list(map(int, [product_price for product_price in similar_products.values_list('price', flat=True)]))
                    average_price = int(mean(prices))
                    data['greatest_average_price'] = int(average_price + average_price/6)
                    data['lowest_average_price'] = int(average_price - average_price/6)

            return JsonResponse(data)
        raise Http404

class DetailView(DetailView):
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_object(self):
        product_class = globals()[self.kwargs.get('section').capitalize()]
        product_slug = self.kwargs.get('product_slug')
        product = product_class.all_objects.select_related('seller', 'city').prefetch_related('images').get(slug=product_slug)

        return product

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        product = self.get_object()

        context['send_email_form'] = forms.SendEmailForm()

        return context

    def get(self, request, *args, **kwargs):
        product = self.get_object()

        if not(product.seller == request.user):
            product.views += 1
            product.save()

        return super(DetailView, self).get(request, *kwargs, **kwargs)

class ObservedProductsView(ListView):
    template_name = 'products/observed_product_list.html'
    context_object_name = 'products'

    def get_observed_cookie_products(self):
        observed_cars = self.request.COOKIES.get('observed_cars')
        observed_cars = Car.objects.filter(id__in=observed_cars.split(',')).select_related('city').prefetch_related('images') if observed_cars else Car.objects.none()

        observed_parts = self.request.COOKIES.get('observed_parts')
        observed_parts = Part.objects.filter(id__in=observed_parts.split(',')).select_related('city').prefetch_related('images') if observed_parts else Part.objects.none()

        observed_motorcycles = self.request.COOKIES.get('observed_motorcycles')
        observed_motorcycles = Motorcycle.objects.filter(id__in=observed_motorcycles.split(',')).select_related('city').prefetch_related('images') if observed_motorcycles else Motorcycle.objects.none()

        return QuerySetSequence(observed_cars, observed_parts, observed_motorcycles).select_related('city').prefetch_related('images')

    @staticmethod
    def get_observed_list(user):
        observed_cars = user.observed_cars.select_related('city').prefetch_related('images').all() if user.observed_cars.exists() else Car.objects.none()
        observed_parts = user.observed_parts.select_related('city').prefetch_related('images').all() if user.observed_parts.exists() else Part.objects.none()
        observed_motorcycles = user.observed_motorcycles.select_related('city').prefetch_related('images').all() if user.observed_motorcycles.exists() else Motorcycle.objects.none()

        return QuerySetSequence(observed_cars, observed_parts, observed_motorcycles).select_related('city').prefetch_related('images')

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return self.get_observed_list(user)
        return self.get_observed_cookie_products()

    def get_context_data(self, *args, **kwargs):
        context = super(ObservedProductsView, self).get_context_data(*args, **kwargs)

        context['observed_products_count'] = self.get_queryset().count()
        if self.request.user.is_authenticated and self.get_observed_cookie_products().exists():
            context['cookie_products'] = self.get_observed_cookie_products()

        return context

class TransportObservedProducts(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            data = {}

            observed_cars = self.request.COOKIES.get('observed_cars')
            if observed_cars:
                cars = Car.objects.filter(id__in=map(int, observed_cars.split(',')))
                user.observed_cars.add(*[product for product in cars])

            observed_parts = self.request.COOKIES.get('observed_parts')
            if observed_parts:
                parts = Part.objects.filter(id__in=map(int, observed_parts.split(',')))
                user.observed_parts.add(*[product for product in parts])

            observed_motorcycles = self.request.COOKIES.get('observed_motorcycles')
            if observed_motorcycles:
                motorcycles = Motorcycle.objects.filter(id__in=map(int, observed_motorcycles.split(',')))
                user.observed_motorcycles.add(*[product for product in motorcycles])

            data['observed_cars'] = observed_cars
            data['observed_parts'] = observed_parts
            data['observed_motorcycles'] = observed_motorcycles

            return JsonResponse(data)
        raise Http404

class AddObservedProduct(View):
    def get(self, request, *args, **kwargs):
        data = {}
        user = request.user

        section = self.kwargs.get('section')
        product_id = self.kwargs.get('product_id')
        product_class = globals()[section.capitalize()]
        product = product_class.objects.get(id=product_id)

        if request.is_ajax():
            observed_list_name = f'observed_{section.lower()}s'
            if user.is_authenticated:
                observed_list = getattr(user, observed_list_name)
                observed_list.add(product.id)
            else:
                data['observed_list_name'] = observed_list_name
                data['product_id'] = product.id

            data['remove_observed_offer'] = reverse('products:remove-observed-offer', kwargs={'section': section, 'product_id': product.id})
            return JsonResponse(data)
        raise Http404

class RemoveObservedProduct(View):
    def get(self, request, *args, **kwargs):
        data = {}
        user = request.user

        section = self.kwargs.get('section')
        product_id = self.kwargs.get('product_id')
        product_class = globals()[section.capitalize()]
        product = product_class.objects.get(id=product_id)

        if request.is_ajax():
            observed_list_name = f'observed_{section.lower()}s'
            if user.is_authenticated:
                observed_list = getattr(user, observed_list_name)
                observed_list.remove(product)

                observed_cars = user.observed_cars.all() if user.observed_cars.exists() else Car.objects.none()
                observed_parts = user.observed_parts.all() if user.observed_parts.exists() else Part.objects.none()
                observed_motorcycles = user.observed_motorcycles.all() if user.observed_motorcycles.exists() else Motorcycle.objects.none()

                if not(ObservedProductsView.get_observed_list(user).exists()):
                    data['last_item'] = True
            else:
                data['observed_list_name'] = observed_list_name
                data['product_id'] = product.id

            data['add_observed_offer'] = reverse('products:add-observed-offer', kwargs={'section': section, 'product_id': product.id})
            return JsonResponse(data)
        raise Http404

class CreateProductView(CreateView):
    template_name = 'products/create_product.html'
    success_url = '/'

    def get_form_class(self):
        section = self.kwargs.get('section').capitalize()
        return getattr(forms, f'Create{section}Form')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.seller = self.request.user
        product.save()

        return super(CreateProductView, self).form_valid(form)

    def form_invalid(self, form):
        print('=-=-=-=-=-=-==-=-=-=')
        print('error')
        print('=-=-=-=-=-=-==-=-=-=')

        return super(CreateProductView, self).form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CreateProductView, self).get_context_data(*args, **kwargs)

        context['section'] = self.kwargs.get('section')

        return context

class DeleteProduct(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}

            product_class = globals()[self.kwargs.get('product_class').capitalize()]
            product_id = self.kwargs.get('product_id')
            product = product_class.all_objects.get(id=product_id)

            if product.seller == request.user:
                product.delete()
                data['message'] = 'success'


































































            return JsonResponse(data)
        raise Http404