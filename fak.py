from mapp.models import *
from accounts.models import CustomUser

from faker import Faker
import names

import nepali_roman as nr

faker = Faker('hi_IN')
# faker.items()

# addr = faker.address()
# naddr = nr.romanize_text(addr)
# print(addr, naddr)
# a = Assignment.objects.get()
# for item in a:
#     print(a)

f = Faker('hi_IN')


def accounts(num=5):
    for _ in range(num):
        city_name = nr.romanize_text(f.city_name())
        street_name = nr.romanize_text(f.street_address())
        postcode = f.postcode()

        name = '{} {}'.format(nr.romanize_text(f.first_name()).capitalize(),
                              nr.romanize_text(f.last_name()).capitalize())
        email = name.replace(' ', '_')+ '@gmail.com'
        addr = '{}, {}-{}'.format(street_name, city_name, postcode)
        phone_number = '+91'+str(f.random_number(10))
        print(name, phone_number, email)
        print(addr)

        obj = CustomUser(
            email=email,
            password='123',
            name=name,
            mobile_number=phone_number,
            job='NA',
            address=addr,
        )
        obj.save()

accounts(2)
