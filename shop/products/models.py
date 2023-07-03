# from django.contrib.gis.db import models
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from django_countries.fields import CountryField
from cities_light.models import Region, City
from phonenumber_field.modelfields import PhoneNumberField

CURRENCY = (
    ('PLN', 'PLN'),
    ('EUR', 'EUR'),
)

GEARBOX = (
    ('manual', _('Manual')),
    ('automatic', _('Automatic')),
    ('half-automatic', _('Half-automatic')),
)

# YEAR_PRODUCTION = (
#     ('2020', 2020),
#     ('2019', 2019),
#     ('2018', 2018),
#     ('2017', 2017),
#     ('2016', 2016),
#     ('2015', 2015),
#     ('2014', 2014),
#     ('2013', 2013),
#     ('2012', 2012),
#     ('2011', 2011),
#     ('2010', 2010),
#     ('1999', 1999),
#     ('1998', 1998),
#     ('1997', 1997),
#     ('1996', 1996),
#     ('1995', 1995),
#     ('1994', 1994),
#     ('1993', 1993),
#     ('1992', 1992),
#     ('1991', 1991),
#     ('1990', 1990),
# )

YEAR_PRODUCTION = []

year = 1990
while year <= timezone.now().year:
    YEAR_PRODUCTION.append((str(year), year))
    year += 1

MARK = (
    ('BMW', 'BMW'),
    ('volkswagen', 'Volksvagen'),
    ('opel', 'Opel'),
    ('audi', 'Audi'),
    ('mercedes-benz', 'Mercedes-benz'),
    ('toyota', 'Toyota'),
)

CONDITION = (
    ('brand_new', _('Brand new')),
    ('used', _('Used')),
)

FUEL_TYPE = (
    ('petrol', _('Petrol')),
    ('disel', 'Disel'),
    ('petrol+LPG', _('Petrol+LPG')),
    ('petrol+CNG', _('Petrol+CNG')),
    ('electric', _('Electric')),
    ('etanol', 'Etanol'),
    ('hybrid', _('Hybrid')),
    ('hydrogen', _('Hydrogen')),
)

COLOR = (
    ('black', _('Black')),
    ('Brown', _('Brown')),
    ('purple', _('Purple')),
    ('red', _('Red')),
    ('blue', _('Blue')),
    ('white', _('White')),
    ('gold', _('Gold')),
    ('silver', _('Silver')),
    ('grey', _('Grey')),
    ('yellow', _('Yellow')),
    ('green', _('Green')),
    ('other_color', _('Other color')),
)

COLOR_OPTION = (
    ('metallic', _('Metallic')),
    ('pearl', _('Pearl')),
    ('mat', _('Mat')),
    ('acrylic-non-metallic)', _('Acrylic (non-metallic)')),
)

DRIVE = (
    ('4x4-auto', _('4x4 (included automatically)')),
    ('4x4-manually', _('4x4 (included manually)')),
    ('4x4-constant', _('4x4 (constant)')),
    ('front-wheels', _('Front wheels')),
    ('back-wheels', _('Back wheels')),
)

CAR_TYPE = (
    ('small_car', _('Small car')),
    ('city_car', _('City car')),
    ('compact', _('Compact')),
    ('sedan', 'Sedan'),
    ('combi', _('Combi')),
    ('minivan', 'Minivan'),
    ('suv', 'SUV'),
    ('cabriolet', _('Cabriolet')),
    ('Coupe', 'Coupe'),
)

PART_TYPE = (
    ('accessories', _('Accessories')),
    ('audio_equipment', _('Audio equipment')),
    ('filters', _('Filters')),
    ('interior_items', _('Interior items')),
    ('wheels', _('Wheels')),
    ('tires', _('Tires')),
    ('heating/ventilation/conditioning', _('Heating/ventilation/conditioning')),
    ('lighting', _('Lighting')),
    ('gearbox', _('Gearbox')),
    ('engine', _('Engine')),
    ('electric_system', _('Electric system')),
    ('braking_system', _('Braking system')),
    ('equipment', _('Equipment')),
    ('other', _('Other')),
)

MOTORCYCLE_TYPE = (
    ('chopper', 'Chopper'),
    ('cruiser', 'Cruiser'),
    ('enduro', 'Enduro'),
    ('patch', _('Patch')),
    ('moped', _('Moped')),
    ('naked', _('Naked')),
    ('quad', 'Quad'),
    ('scooter', _('Scooter')),
    ('sporty', _('Sporty')),
    ('tourist', _('Tourist')),
)

class ProductManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(ProductManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only is None:
            return models.QuerySet(self.model)
        elif self.alive_only is True:
             return models.QuerySet(self.model).filter(delete_at__gt=timezone.now())
        return models.QuerySet(self.model).filter(delete_at__lte=timezone.now())

class BaseProduct(models.Model):
    delete_at = models.DateField(auto_now_add=True)

    # Untaged
    raise_list_times = models.PositiveSmallIntegerField(default=0)
    colorful_list_days = models.DateField(verbose_name='Colorful list days', blank=True, null=True)
    promo_days = models.DateField(verbose_name='Promoted days', blank=True, null=True)

    slug = models.SlugField(max_length=160, allow_unicode=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    price = models.DecimalField(verbose_name='Price', max_digits=9, decimal_places=2, default=0)
    currency = models.CharField(verbose_name='Currency', max_length=3, choices=CURRENCY, default='PLN')
    pub_date = models.DateTimeField(verbose_name='Published day', auto_now_add=True)
    phonenumber_views = models.PositiveIntegerField(default=0)

    # Boolean fields
    negotiate = models.BooleanField(verbose_name='Is price to negotiate', default=False)
    price_netto = models.BooleanField(verbose_name='Price netto (+23% VAT)', default=False)

    # Not required
    description = models.TextField(verbose_name='Description', max_length=4096, blank=True, null=True)
    youtube_link = models.URLField(verbose_name='Youtube video', blank=True, null=True)
    warranty = models.DateField(verbose_name='Warranty', blank=True, null=True)

    # Required
    mark = models.CharField(verbose_name='Mark', max_length=13, choices=MARK)
    condition = models.CharField(verbose_name='Condition', max_length=9, choices=CONDITION)
    first_name = models.CharField(verbose_name='First name', max_length=35)
    phonenumber = PhoneNumberField(verbose_name='Phonenumber')
    email = models.EmailField(verbose_name='Email', max_length=60)
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.CASCADE)

    objects = ProductManager()
    all_objects = ProductManager(alive_only=None)
    pending_objects = ProductManager(alive_only=False)

    class Meta:
        abstract = True

class BaseVehicle(BaseProduct):
    # Boolean fields
    first_owner = models.BooleanField(verbose_name='Is first owner', default=False)

    # Not required
    title = models.CharField(verbose_name='Title', max_length=200, blank=True, null=True)
    registeration_num = models.CharField(verbose_name='Registeration number', max_length=15, blank=True, null=True)
    color_option = models.CharField(max_length=21, choices=COLOR_OPTION, blank=True, null=True)
    co2_emission = models.PositiveIntegerField(verbose_name='CO2 Emission', blank=True, null=True)
    particulate_filter = models.BooleanField(verbose_name='Particulate filter', default=False)
    country_of_origin = CountryField(verbose_name='Country of origin', blank=True, null=True)
    first_registeration = models.DateField(verbose_name='First Registeration', blank=True, null=True)

    # Required
    mileage = models.PositiveIntegerField(verbose_name='Mileage')
    power = models.PositiveIntegerField(verbose_name='Power')
    color = models.CharField(verbose_name='Color', max_length=11, choices=COLOR)
    gearbox = models.CharField(verbose_name='Gearbox', max_length=14, choices=GEARBOX)
    year_production = models.CharField(verbose_name='Year production', max_length=4, choices=YEAR_PRODUCTION)

    class Meta:
        abstract = True

class Car(BaseVehicle):
    # Untaged
    seller = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='cars')

    # BooleanFields
    right_hand_drive = models.BooleanField(verbose_name='right hand drive (England)', default=False)

    # Not required
    num_of_doors = models.PositiveIntegerField(verbose_name='number of doors', blank=False, null=False)
    num_of_seats = models.PositiveIntegerField(verbose_name='number of seats', blank=True, null=True)
    drive = models.CharField(verbose_name='Drive', max_length=12, choices=DRIVE, blank=True, null=True)

    # Required
    car_type = models.CharField(verbose_name='Type of car', max_length=9, choices=CAR_TYPE)
    fuel_type = models.CharField(verbose_name='Fuel type', max_length=10, choices=FUEL_TYPE)

    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.mark}-{self.year_production}-{self.color}-{self.gearbox}-{self.fuel_type}-{self.condition}-{self.id}')
            self.save()

    def get_title(self):
        return f"{self.get_mark_display()}, {self.year_production}, {self.get_fuel_type_display()} {self.title if self.title else ''}".strip()

    def __str__(self):
        return self.get_title()

class ImageCar(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/cars/%Y/%m/%d/')

    def __str__(self):
        return self.image.url

class Part(BaseProduct):
    seller = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='parts')
    delivery = models.BooleanField(verbose_name='Delivery', default=False)
    title = models.CharField(verbose_name='Title', max_length=200)
    mark = models.CharField(verbose_name='Mark', max_length=13, choices=MARK, blank=True, null=True)
    part_type = models.CharField(verbose_name='Type of part', choices=PART_TYPE, max_length=32)

    def save(self, *args, **kwargs):
        super(Part, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.mark if self.mark else ""} {self.condition}-{self.id}')
            self.save()

    @property
    def get_title(self):
        return self.title

    def __str__(self):
        return self.get_title

class ImagePart(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/parts/%Y/%m/%d/')

    def __str__(self):
        return self.image.url

class Motorcycle(BaseVehicle):
    seller = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='motorcycles')
    motorcycle_type = models.CharField(verbose_name='Type of motocycle', max_length=7, choices=MOTORCYCLE_TYPE)

    def save(self, *args, **kwargs):
        super(Motorcycle, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.mark}-{self.motorcycle_type}-{self.year_production}-{self.color}-{self.gearbox}-{self.condition}-{self.id}')
            self.save()

    def get_title(self):
        return f"{self.get_mark_display()} {self.get_motorcycle_type_display()}, {self.get_condition_display()} {self.title if self.title else ''}".strip()

    def __str__(self):
        return self.get_title()

class ImageMotorcycle(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/motorcycles/%Y/%m/%d/')

    def __str__(self):
        return self.image.url