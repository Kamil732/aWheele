from django.core.management.base import BaseCommand
from django.utils import timezone

import random

from faker import Faker
# from faker.providers.address.pl_PL import Provider
from accounts.models import Account
from cities_light.models import City
from cities_light.loading import CITIES
from products.models import Part, MARK, CONDITION, PART_TYPE

COUNTRY_OF_ORIGIN = ['GE', 'US', 'IT']

class Command(BaseCommand):
    args = '<foo bar ...>'

    def _create_tags(self):
        # p = Provider()
        f = Faker('pl_PL')
        seller = Account.objects.get(email='kamilkamil5542@wp.pl')
        email = 'kamilkamil554@wp.pl'
        delete_at = timezone.now() + timezone.timedelta(days=365)

        parts = []

        for i in range(400):
            price = f.random_int(1500, 240000)
            promo_days = f.date_time_between(start_date='-30d', end_date=timezone.now() + timezone.timedelta(days=90))
            colorful_list_days = f.date_time_between(start_date='-25d', end_date=timezone.now() + timezone.timedelta(days=30))
            negotiate = f.boolean(chance_of_getting_true=43)
            delivery = f.boolean(chance_of_getting_true=65)
            condition = random.choice(CONDITION)[0]
            part_type = random.choice(PART_TYPE)[0]
            title = f.sentence(nb_words=4)
            description = f.paragraph(nb_sentences=10)
            first_name = f.first_name()
            phonenumber = '+48 ' + f.phone_number()
            mark = random.choice(MARK)[0] if f.boolean(chance_of_getting_true=60) else None
            city = City.objects.get(slug=random.choice(CITIES)[0])

            part = Part.objects.create(
                delete_at=delete_at, price=price, negotiate=negotiate, title=title, description=description, first_name=first_name, phonenumber=phonenumber, email=email, \
                city=city, seller=seller, condition=condition, mark=mark, promo_days=promo_days, colorful_list_days=colorful_list_days, \
                part_type=part_type, delivery=delivery
            )

            parts.append(part)

            # Car.objects.create(price=price, num_of_doors=4, first_name=first_name, phonenumber=phonenumber, condition='used', mileage=100000, email=email, power=240, city=city, seller=seller, color=color, year_production='2017', gearbox='manual', drive=drive, fuel_type='petrol', country_of_origin=country_of_origin, mark='BMW', promo_days=promo_days, colorful_list_days=colorful_list_days)

        for part in parts:
            part.delete_at = delete_at
            part.save()

    def handle(self, *args, **options):
        print('\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=')
        print('Wait\n')
        try:
            self._create_tags()
        finally:
            print('complete!')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=')