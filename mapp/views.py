from datetime import datetime
import reusables
from django.forms import formset_factory
from django.conf import settings
from django.contrib import messages
from termcolor import cprint
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.shortcuts import render, get_object_or_404
from django.urls import resolve
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone

from .models import *
from .forms import *
from accounts.models import CustomUser
from django.db.models import Sum


# TODO forms for assigment viewer


@login_required
def portfolioView(request, **kwargs):
    print("called for pro")
    print(kwargs['id'])
    # return HttpResponseRedirect(reverse('mapp:portfolio'))
    return render(request, 'mapp/handyman_portfolio.html',
                  {'handyman': CustomUser.objects.get(id=kwargs['id'])})


def adv_edit_view(request, **kwargs):
    template_name = 'mapp/advertisment_form.html'
    if request.method == 'GET':
        if 'id' in kwargs.keys():
            id = kwargs['id']
            adv_obj = Advertisment.objects.get(pk=id)
            advForm = AdverstimentForm(initial={'title': adv_obj.title,
                                                'image': adv_obj.image,
                                                'task': adv_obj.task,
                                                'description': adv_obj.description,
                                                'category': adv_obj.category,
                                                })
            print(len(adv_obj.services.all()))
            Formset = formset_factory(ServicePriceForm, extra=1)
            formset = Formset(initial=[{'name': x.name, 'price': x.price} for x in adv_obj.services.all()])

            # advForm.fields['title'].widget.attrs('value','aslk')
    elif request.method == 'POST':
        advForm = AdverstimentForm(request.POST, request.FILES)
        formset = service_formset(request.POST)
        print("post")
        # print(advForm)
        if 'id' in kwargs.keys() and formset.is_valid() and advForm.is_bound and len(
                advForm.errors) <= 1:

            print(formset.cleaned_data)
            advForm_data = advForm.cleaned_data
            services = {item.get('name'): item.get('price') for item in formset.cleaned_data
                        if item != None and item.get('name') != None and item.get('price') != None}
            # print(services)

            for item in formset.cleaned_data:
                print(111, item, item.get('name'), item.get('price'))
            # print(advForm_data)

            advObj = Advertisment.objects.get(pk=kwargs['id'])

            if 'title' in advForm_data.keys():
                advObj.title = advForm_data.get('title')
            if 'category' in advForm_data.keys():
                advObj.category = advForm_data.get('category')
            if 'task' in advForm_data.keys():
                advObj.task = advForm_data.get('task')
            if 'description' in advForm_data.keys():
                advObj.description = advForm_data.get('description')
            if 'image' in advForm_data.keys():
                advObj.image = advForm_data.get('image')

            # print(advObj, 11)
            advObj.save()
            # print(services)
            for s in advObj.services.all():
                s.delete()
            advObj.services.clear()

            for k, v in services.items():
                s = Service(name=k, price=v)
                s.save()
                print(k, v)
                advObj.services.add(s)

            advObj.save()
            messages.success(request, 'Advertisment Form Successfully Updated')
            return redirect('mapp:handyman_adv')
        else:
            messages.warning(request, 'There is a problem with the form')
        return redirect('mapp:advertisment_form')

    return render(request, template_name, {
        'form': advForm,
        'formset': formset,
    })


def adv_view(request, **kwargs):
    template_name = 'mapp/advertisment_form.html'
    if request.method == 'GET':
        if 'id' in kwargs.keys():
            id = kwargs['id']
            adv_obj = Advertisment.objects.get(pk=id)
            advForm = AdverstimentForm(initial={'title': adv_obj.title,
                                                'image': adv_obj.image,
                                                'task': adv_obj.task,
                                                'description': adv_obj.description,
                                                'category': adv_obj.category,
                                                })
            print(len(adv_obj.services.all()))
            Formset = formset_factory(ServicePriceForm, extra=0)
            formset = Formset(initial=[{'name': x.name, 'price': x.price} for x in adv_obj.services.all()])

            # advForm.fields['title'].widget.attrs('value','aslk')
        else:
            advForm = AdverstimentForm(request.GET or None)
            formset = service_formset()
    elif request.method == 'POST':
        advForm = AdverstimentForm(request.POST, request.FILES)
        formset = service_formset(request.POST)
        print("post")
        # print(advForm)
        if advForm.is_valid() and formset.is_valid():
            print(formset.cleaned_data)
            advForm_data = advForm.cleaned_data
            services = {item.get('name'): item.get('price') for item in formset.cleaned_data
                        if item != None and item.get('name') != None and item.get('price') != None}
            print(services)
            for item in formset.cleaned_data:
                print(111, item, item.get('name'), item.get('price'))
            # print(advForm_data)
            print(type(advForm_data.get('image')))
            advObj = Advertisment(
                title=advForm_data.get('title'),
                handyman=request.user,
                category=advForm_data.get('category'),
                task=advForm_data.get('task'),
                description=advForm_data.get('description'),
                image=advForm_data.get('image')
            )
            print(advObj, 11)
            advObj.save()
            print(services)
            for k, v in services.items():
                s = Service(name=k, price=v)
                s.save()
                print(k, v)
                advObj.services.add(s)

            advObj.save()
            messages.success(request, 'Advertisment Form Successfully saved')
            return redirect('mapp:home')
        else:
            messages.warning(request, 'There is a problem with the form')
        return redirect('mapp:advertisment_form')

    return render(request, template_name, {
        'form': advForm,
        'formset': formset,
    })


class HomeView(ListView):
    # model = Advertisment
    # print(model.image)
    paginate_by = 5
    template_name = "mapp/home.html"

    # queryset = model.objects.filter(category='CA')
    # def get(self, request, **kwargs):
    #     print("Got in get")
    #

    def get_queryset(self):
        # self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])

        try:
            print("#Debug Inside Homeview, get_queryset(): query=", self.request.GET['search'])
            return Advertisment.objects.filter(title__contains=self.request.GET['search'])
        except:
            pass

        try:
            print('Up here')
            print(self.kwargs['category'])
            return Advertisment.objects.filter(category=self.kwargs['category'])
        except:
            pass
        return Advertisment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['cat'] = self.kwargs['category']
        except:
            pass
        return context


class AdvertismentDetailView(FormMixin, DetailView):
    model = Advertisment
    template_name = "mapp/detail.html"
    form_class = ServiceForm

    def book_adv(self):
        print("Book")

    def get_context_data(self, **kwargs):
        # print(self.request.GET)
        # print('got here################################################################')
        # Call the base implementation first to get a context
        context = super(AdvertismentDetailView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        context['extra'] = context['advertisment'].services.all()
        context['form'] = ServiceForm(initial={'post': self.object})

        # Check for if the user doesn't have a address or if the user is a guest
        try:
            context['form'].fields['address'].widget.attrs['value'] = self.request.user.address
        except AttributeError:
            context['form'].fields['address'].widget.attrs['value'] = ' '

        # context['form'].fields['services'].choices = [(s.nameSlug, s.name) for s in self.object.getServices()]
        # print(context['form'])
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        # form = ServiceForm(self.request.POST or None)
        print(request.POST, '*')
        # print(type(adv_obj))
        # print(form)

        # Add the data to assignment model
        post_data = dict(request.POST)
        if 'csrfmiddlewaretoken' in post_data.keys():
            print(post_data.get('appointment_date')[0], post_data.get('services'), post_data.get('address')[0])
            # form = ServiceForm(self.request.POST or None)

            address = post_data.get('address')[0].strip()
            appointment_date = datetime.strptime(post_data.get('appointment_date')[0], '%d/%m/%Y %H:%M')
            services = post_data.get('services')
            adv_obj = self.object
            # datetime.strptime('02/04/2020 12:20', '%d/%m/%Y %H:%M')
            services_obj = [Service.objects.get(nameSlug=service_slug) for service_slug in services]

            new_assignment_obj = Assignment(
                advertisment_id=adv_obj,
                handyman=adv_obj.handyman,
                client=request.user,
                booking_date=timezone.now(),
                price=sum([service.price for service in services_obj]),
                appointment_date=appointment_date,
                address=address
            )

            new_assignment_obj.save()
            new_assignment_obj.services.add(*services_obj)  ##add services
            new_assignment_obj.save()

        if form.is_valid():
            cprint('Valid Form', 'green')
            return self.form_valid(form)
        else:
            cprint('Invalid Form', 'blue')
            return self.form_valid(form)
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))

    def form_valid(self, form):
        # print(form)
        # print('get values')
        # print(form.cleaned_data.get('address'), form.cleaned_data.get('appointment_date'), form.cleaned_data.get('services'))
        # form.save()
        return self.render_to_response(self.get_context_data(form=form))
        # return super(AdvertismentDetailView, self).form_valid(form)


class AssignmentView(ListView):
    template_name = "mapp/assignments.html"
    model = Assignment

    def get_queryset(self):
        return Assignment.objects.filter(client=self.request.user)


class WorkView(ListView):
    template_name = "mapp/work.html"
    model = Assignment

    def get_queryset(self):
        return Assignment.objects.filter(handyman=self.request.user)


class HandymanAdvView(ListView):
    template_name = "mapp/handyman_adv_list.html"
    model = Advertisment

    def get_queryset(self):
        return Advertisment.objects.filter(handyman=self.request.user)


# def assigm(request):
#     return render(request, 'mapp/assignments.html')

# def get(self, request, *args, **kwargs):
# return Assignment.objects.filter(client=self.request.user)

# def search(request):
#     print("Search function")
#     if request.method == 'GET':  # this will be GET now
#         keyword = request.GET.get('key')  # do some research what it does
#         try:
#             status = Advertisment.objects.filter(bookname__icontains=keyword)
#         except:
#             pass
#         return render(request, "mapp/search.html", {"adv": status})
#     else:
#         return render(request, "mapp/search.html", {})

# # from django import forms


# # Create your views here.
# #
# # def hi(request):
# #     namelst= Students.objects.order_by('sid')
# #     my_dict = {'rec': namelst}
# #     my_dict = {'insert_me': 'Hello this is first page'}
# #     return render(request, 'mapp/hi.html')
# #
# #
# # def form_view(request):
# #     form = forms_html.main_form()
# #
# #     if request.method == 'POST':
# #         form = forms_html.main_form(request.POST)
# #
# #         if form.is_valid():
# #             print("Validated ")
# #             print("name", form.cleaned_data['name'])
# #             print("sid", form.cleaned_data['sid'])
# #             print("number", form.cleaned_data['number'])
# #
# #     return render(request, 'mapp/index.html', {'form': form})
# #
# #
# # def second_form_view(request):
# #     form = second_form()
# #     if request.method == "POST":
# #         form = second_form(request.POST)
# #
# #         if form.is_valid():
# #             print("Valid form")
# #             form.save(commit=True)
# #             return hi(request)
# #         else:
# #             print("Error: Invalid Form")
# #
# #     return render(request, 'mapp/index.html', {'form': form})


# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {
#                 'object': order
#             }
#             return render(self.request, 'mapp/assignments.html', context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("/")


# class CheckoutView(View):
#     def get(self, *args, **kwargs):
#         form = CheckoutForm()
#         context = {
#             'form': form
#         }

#         return render(self.request, "mapp/checkout.html", context)

#     def post(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         form = CheckoutForm(self.request.POST or None)
#         if form.is_valid():
#             shipping_address1 = form.cleaned_data.get(
#                 'shipping_address')
#             shipping_address2 = form.cleaned_data.get(
#                 'shipping_address2')
#             shipping_country = form.cleaned_data.get(
#                 'shipping_country')
#             shipping_zip = form.cleaned_data.get('shipping_zip')
#             shipping_address = Address(
#                 user=self.request.user,
#                 street_address=shipping_address1,
#                 apartment_address=shipping_address2,
#                 country=shipping_country,
#                 zip=shipping_zip,
#                 address_type='S')
#             shipping_address.save()
#             order.shipping_address = shipping_address

#             billing_address1 = form.cleaned_data.get(
#                 'billing_address')
#             billing_address2 = form.cleaned_data.get(
#                 'billing_address2')
#             billing_country = form.cleaned_data.get(
#                 'billing_country')
#             billing_zip = form.cleaned_data.get('billing_zip')
#             billing_address = Address(
#                 user=self.request.user,
#                 street_address=shipping_address1,
#                 apartment_address=shipping_address2,
#                 country=shipping_country,
#                 zip=shipping_zip,
#                 address_type='B')
#             billing_address.save()
#             order.billing_address = billing_address

#             # order.ordered = True
#             order.save()
#             print("Checkout Form is valid")
#             return redirect('mapp:payment')
#         return redirect('mapp:home')


# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         context = {
#             'order': order,
#             'DISPLAY_COUPON_FORM': False
#         }
#         return render(self.request, "mapp/payment.html", context)

#     def post(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         form = PaymentForm(self.request.POST)

#         order_items = order.items.all()
#         order_items.update(ordered=True)
#         for item in order_items:
#             item.save()
#         order.ordered = True
#         order.save()

#         return redirect('mapp:order-summary')

@login_required
def book(request, slug):
    print('book')

    if request.method == 'POST':
        print('post ho ')
        print(request.POST)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))

    adv = get_object_or_404(Advertisment, slug=slug)
    print("booking for ", adv, ': ', request.user)
    book_item, created = Assignment.objects.get_or_create(client=request.user,
                                                          advertisment_id=adv,
                                                          handyman=adv.handyman
                                                          )
    # print(book_item, created)
    book_item.save()
    messages.success(request, f"{adv.title} has been booked.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))


@login_required
def unbook(request, id):
    print("Unbook")
    adv = Assignment.objects.get(advertisment_id=id, client=request.user)
    title = adv.advertisment_id.title
    adv.delete()
    messages.warning(request, f"{title} has been unbooked.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))

# @login_required
# def add_to_cart(request, slug):
#     # slug is the item that user want to order
#     item = get_object_or_404(Item, slug=slug)

#     # it creates a OrderItem object for that item
#     order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, ordered=False)

#     # Get the current non ordered order query list
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # Check if order item is in the order item__slug is the slugs in the order, and item.slug is the slug of item
#         # added to the cart

#         # if the orderitem is present in the cart increase the quantiy
#         if order.items.filter(item__slug=item.slug).exists():
#             print("increase product")
#             order_item.quantity += 1
#             order_item.save()
#             messages.warning(request, f"{item.title} quantity has updated.")
#             # return HttpResponseRedirect("#")
#             # return redirect("mapp:product", slug=slug)
#         else:
#             # else create a orderitem in cart
#             messages.warning(request, f"{item.title} has been added to card.")
#             order.items.add(order_item)
#             # return redirect("mapp:product", slug=slug)

#     else:
#         # if the user has no cart at all, create a new cart object for hte user
#         ordered_date = timezone.now()
#         order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         messages.warning(request, f"{item.title} has been added to card.")
#         # return redirect("mapp:product", slug=slug)

#     return redirect("mapp:order-summary")


# @login_required
# def remove_from_cart(request, slug):
#     print("reached remove from cart", request.user)
#     item = get_object_or_404(Item, slug=slug)
#     current_url = resolve(request.path_info).url_name
#     print(current_url)
#     # order_qs = Order.objects.filter(user=request.user, ordered=False)

#     # Decrease OderItem quantity or remove the OrderItem object
#     order_item_qs = OrderItem.objects.filter(user=request.user, item=item)
#     if order_item_qs.exists():
#         order_item = order_item_qs[0]

#         # Checking the cart quantity
#         if order_item.quantity > 1:
#             order_item.quantity -= 1
#             order_item.save()
#             messages.warning(request, "This item quantity was updated.")
#             # return redirect("mapp:product", slug=slug)
#             # return redirect("mapp:product", slug=slug)
#         else:
#             order_item_qs.delete()
#             messages.warning(request, "This item was removed from the cart")

#             # return redirect("mapp:product", slug=slug)
#     else:
#         messages.warning(request, "This item is not in your cart")

#     return redirect("mapp:order-summary")

#     # order_qs = Order.objects.filter(user=request.user)
#     # if not order_qs.exists():
#     #     # return redirect("mapp:product", slug=slug)
#     #     order_qs.delete()

#     # order_qs = Order.objects.filter(user=request.user, ordered=False)
#     #     # if order_qs.exists():
#     #     #     order = order_qs[0]
#     #     #     if order.items.filter(item__slug=item.slug).exists():
#     #     #         order_item = OrderItem.objects.filter(user=request.user, ordered=False)[0]
#     #     #         order.items.remove(order_item)
#     #     #     else:
#     #     #         # messages.warning(request, "This item was not in your cart")
#     #     #         return redirect("mapp:product", slug=slug)
#     #     # else:
#     #     #     # messages.warning(request, "You do not have an active order")
#     #     #     return redirect("mapp:product", slug=slug)


# def index(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'mapp/home.html', context=context)


# def info(request):
#     return render(request, 'mapp/info.html')


# def item_list(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     print([x for x in Item.objects.all()])
#     return render(request, "item_list.html", context=context)

# def register(request):
#     registered = False
#     print("Got here", registered)
#     if request.method == "POST":
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'profile_pic' in request.FILES:
#                 profile.profile_pic = request.FILES['profile_pic']
#
#             profile.save()
#
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileInfoForm()
#
#     return render(request, 'mapp/register.html',
#                   {'registered': registered, 'user_form': user_form, 'profile_form': profile_form})
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('mapp:index'))
#
#
# def user_login(request):
#
#     if request.method == "POST":
#         username= request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('mapp:index'))
#             else:
#                 return HttpResponse("Account not active")
#         else:
#             print("Some tried to login and failed!")
#             print("Username {} and password {}".format(username, password))
#             HttpResponse("Invalid login details")
#     else:
#         return render(request, 'mapp/login.html')
