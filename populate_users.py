import os

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm_proj.settings')

import django

# Import settings
django.setup()

from products.models import Product
from faker import Faker

fakegen = Faker()


def populate(N=5):
    '''
    Create N Entries of Dates Accessed
    '''

    for entry in range(N):
        # Create Fake Data for entry
        fake_name = fakegen.name().split()
        fake_first_name = fake_name[0]
        fake_last_name = fake_name[1]
        fake_email = fakegen.email()

        # Create new User Entry
        user = Product.objects.get_or_create(name=fakegen.company(), slug=fakegen.slug(), category_id='tshirt',
                                             preview_text=fakegen.word(),
                                             detail_text=fakegen.text(max_nb_chars=100, ext_word_list=None),
                                             price=fakegen.random.randint(1, 10))


if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate(5)
    print('Populating Complete')
