import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from stdimage.models import JPEGField


from m_proj import settings

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


class Message(models.Model):
    text = models.CharField(max_length=1024)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')

    def __str__(self):
        if not self.text:
            return ' '


class Chat(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_client')
    handyman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_handyman')
    message = models.ManyToManyField(Message)


class Service(models.Model):
    name = models.CharField(max_length=255)
    nameSlug = models.SlugField(unique=True, max_length=255)
    # abbreviation = models.CharField(max_length=3)
    price = models.FloatField()

    def save(self, *args, **kwargs):
        s = slugify(self.name) + str(uuid.uuid4())
        self.nameSlug = s
        print(self.nameSlug)
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
        ordering = ['-appointment_date']
