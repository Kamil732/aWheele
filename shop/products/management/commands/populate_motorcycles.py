from django.core.management.base import BaseCommand
from django.utils import timezone

import random

from faker import Faker
# from faker.providers.address.pl_PL import Provider
from accounts.models import Account
from cities_light.models import City
from cities_light.loading import CITIES
from products.models import Motorcycle, MARK, CONDITION, COLOR, GEARBOX, YEAR_PRODUCTION, MOTORCYCLE_TYPE

COUNTRY_OF_ORIGIN = ['GE', 'US', 'IT']

class Command(BaseCommand):
    args = '<foo bar ...>'

    def _create_tags(self):
        # p = Provider()
        f = Faker('pl_PL')
        seller = Account.objects.get(email='kamilkamil5542@wp.pl')
        email = 'kamilkamil554@wp.pl'

        for i in range(200):
            price = f.random_int(1500, 240000)
            promo_days = f.date_time_between(start_date='-30d', end_date=timezone.now() + timezone.timedelta(days=f.random_int(2, 90)))
            colorful_list_days = f.date_time_between(start_date='-25d', end_date=timezone.now() + timezone.timedelta(days=f.random_int(2, 30)))
            negotiate = f.boolean(chance_of_getting_true=43)
            condition = random.choice(CONDITION)[0]
            color = random.choice(COLOR)[0]
            motorcycle_type = random.choice(MOTORCYCLE_TYPE)[0]
            year_production = random.choice(YEAR_PRODUCTION)[0]
            gearbox = random.choice(GEARBOX)[0]
            description = f.paragraph(nb_sentences=10)
            first_name = f.first_name()
            phonenumber = '+48 ' + f.phone_number()
            first_owner = f.boolean(chance_of_getting_true=35)
            mark = random.choice(MARK)[0]
            mileage = f.random_int(500, 250000)
            power = f.random_int(120, 390)
            country_of_origin = random.choice(COUNTRY_OF_ORIGIN)
            city = City.objects.get(slug=random.choice(CITIES)[0])

            Motorcycle.objects.create(
                price=price, negotiate=negotiate, description=description, first_name=first_name, phonenumber=phonenumber, \
                email=email, first_owner=first_owner, mileage=mileage, power=power, city=city, seller=seller, condition=condition, \
                color=color, motorcycle_type=motorcycle_type, year_production=year_production, gearbox=gearbox, country_of_origin=country_of_origin, \
                mark=mark, promo_days=promo_days, colorful_list_days=colorful_list_days
            )
            # Car.objects.create(price=price, num_of_doors=4, first_name=first_name, phonenumber=phonenumber, condition='used', mileage=100000, email=email, power=240, city=city, seller=seller, color=color, year_production='2017', gearbox='manual', drive=drive, fuel_type='petrol', country_of_origin=country_of_origin, mark='BMW', promo_days=promo_days, colorful_list_days=colorful_list_days)

    def handle(self, *args, **options):
        print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=')
        print('Wait\n')
        try:
            self._create_tags()
        finally:
            print('complete!')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=')