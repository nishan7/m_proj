import uuid

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from m_proj import settings
from stdimage.models import StdImageField, JPEGField

CATEGORY_CHOICES = (
    ('CA', 'Carpenter'),
    ('PL', 'Plumber'),
    ('EL', 'Electrician'),
    ('AC', 'Installations & Repairs'),
    ('PA', 'Painters'),
    ('CL', 'Cleaning'),
    ('PT', 'Pest Control'),
    ('MC', 'Misc')
)


class Service(models.Model):
    name = models.CharField(max_length=255)
    nameSlug = models.SlugField(unique=True)
    # abbreviation = models.CharField(max_length=3)
    price = models.FloatField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + str(uuid.uuid4())[:49]
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        if self.price != 0:
            return '{} \u20B9{}'.format(self.name, self.price)
        return '{} \u20B9'.format(self.name)

    class Meta:
        db_table = "Service"
        ordering = ['-price']


class Advertisment(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    # label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    handyman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postdate = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100)
    task = models.CharField(max_length=200)
    description = models.TextField()
    image = JPEGField(upload_to="", variations={
        'thumbnail': {"width": 400, "height": 250, "crop": True}})
    services = models.ManyToManyField(Service)

    def save(self, *args, **kwargs):
        slug = slugify(self.title) + str(uuid.uuid4())
        self.slug = slug[:50]
        super(Advertisment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("mapp:detail", kwargs={
            'slug': self.slug
        })

    def is_booked(self, data):
        print('is booked ', data)
        return True

    def getHandymanName(self):
        return self.handyman.get_cache_name()

    def book(self):
        print("reached here book")
        return reverse("mapp:book", kwargs={
            'slug': self.slug
        })

    def unbook(self):
        return reverse("mapp:unbook", kwargs={
            'id': self.id
        })

    def getServices(self):
        return self.services.all()

    def __str__(self):
        return self.title + ' by ' + self.handyman.get_cache_name()

    class Meta:
        db_table = "Advertisment"
        ordering = ['-postdate']


class Assignment(models.Model):
    advertisment_id = models.ForeignKey(Advertisment, on_delete=models.CASCADE)
    handyman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='handyman')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client')
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    appointment_date = models.DateTimeField(blank=True, null=True)
    durations = models.TimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    address = models.CharField(max_length=200, blank=True)
    services = models.ManyToManyField(Service)

    # a = Assignment()
    # a.save()
    # a.services.add(service_obj)
    # a.save(), a.services.all()

    def __str__(self):
        return self.advertisment_id.title + ' for ' + self.client.get_cache_name()

    class Meta:
        db_table = "Assignment"
        ordering = ['appointment_date']

# # Create your models here.
# # class Students(models.Model):
# #     sid = models.IntegerField()
# #     name = models.CharField(max_length=254)
# #     number = models.CharField(max_length=245)
# #
# #     class Meta:
# #         db_table = "students"
# #
# #
# # class UserProfileInfo(models.Model):
# #
# #     # Create relationship (don't inherit from User!)
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #
# #     # Add any additional attributes you want
# #     portfolio_site = models.URLField(blank=True)
# #     # pip install pillow to use this!
# #     # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
# #     profile_pic = models.ImageField(upload_to='basic_app/profile_pics',blank=True)
# #
# #     def __str__(self):
# #         # Built-in attribute of django.contrib.auth.models.User !
# #         return self.user.username

# CATEGORY_CHOICES = (
#     ('S', 'Shirt'),
#     ('SW', 'Sports Wear'),
#     ('OW', 'Outwear')
# )

# LABEL_CHOICES = (
#     ('P', 'primary'),
#     ('S', 'secondary'),
#     ('D', 'danger')
# )

# ADDRESS_CHOICES = (
#     ('B', 'Billing'),
#     ('S', 'Shipping'),
# )


# # list of all the item available in the site
# class Item(models.Model):
#     title = models.CharField(max_length=100)
#     price = models.FloatField()
#     discount_price = models.FloatField(blank=True, null=True)
#     category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
#     label = models.CharField(choices=LABEL_CHOICES, max_length=1)
#     slug = models.SlugField()
#     description = models.TextField()
#     image = models.ImageField(upload_to="")

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse("mapp:product", kwargs={
#             'slug': self.slug
#         })

# def get_add_to_cart_url(self):
#     return reverse("mapp:add-to-cart", kwargs={
#         'slug': self.slug
#     })

#     def get_remove_from_cart_url(self):
#         return reverse("mapp:remove-from-cart", kwargs={
#             'slug': self.slug
#         })


# # List of items with quantity ordered by the user
# class OrderItem(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.item.title}"

#     def get_total_item_price(self):
#         return self.quantity * self.item.price

#     def get_total_discount_item_price(self):
#         return self.quantity * self.item.discount_price

#     def get_amount_saved(self):
#         return self.get_total_item_price() - self.get_total_discount_item_price()

#     def get_final_price(self):
#         if self.item.discount_price:
#             return self.get_total_discount_item_price()
#         return self.get_total_item_price()


# # cart order of the indiviual
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ref_code = models.CharField(max_length=20, blank=True, null=True)
#     items = models.ManyToManyField(OrderItem)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)
#     shipping_address = models.ForeignKey(
#         'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
#     billing_address = models.ForeignKey(
#         'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)

#     def __str__(self):
#         return self.user.get_cache_name()

#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_final_price()
#         # if self.coupon:
#         #     total -= self.coupon.amount
#         return total


# class Address(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)
#     street_address = models.CharField(max_length=100)
#     apartment_address = models.CharField(max_length=100)
#     country = CountryField(multiple=False)
#     zip = models.CharField(max_length=100)
#     address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
#     default = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.get_cache_name()
