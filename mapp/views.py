from datetime import datetime, timedelta

import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from termcolor import cprint

from accounts.models import CustomUser, Dates
from .forms import *
from .models import *


# TODO forms for assigment viewer


# View to chat with handyman or client
def chat(request, **kwargs):
    if request.user.is_handyman:
        client_obj = CustomUser.objects.get(pk=kwargs['user_id'])
        handyman_obj = request.user
        senderName = handyman_obj.get_first_name()
        receiverName = client_obj.get_first_name()
    else:
        client_obj = request.user
        handyman_obj = CustomUser.objects.get(pk=kwargs['user_id'])
        senderName = client_obj.get_first_name()
        receiverName = handyman_obj.get_first_name()

    if request.method == 'POST':
        message = request.POST['message']
        sender = request.user
        message_obj = Message(text=message, sender=sender)
        message_obj.save()
        chat, _ = Chat.objects.get_or_create(client=client_obj, handyman=handyman_obj)
        print(chat)
        chat.message.add(message_obj)
        chat.save()

    try:
        chat = Chat.objects.get(client=client_obj, handyman=handyman_obj)
    except:
        messages = []
        return render(request, 'mapp/chat.html',
                      {'chat_messages': messages, 'sender': senderName, 'reciever': receiverName})

    if chat:
        # Store the messages in the list, True in sender means the user which request page has written this particular
        # message
        messages = [(message.text, str(message.sender_id) == str(request.user.id)) for message in chat.message.all()]

    else:
        messages = []
    print(messages)

    return render(request, 'mapp/chat.html',
                  {'chat_messages': messages, 'sender': senderName, 'reciever': receiverName})


@login_required
# View about the detail info about the handyman
def portfolioView(request, **kwargs):
    print("called for pro")
    print(kwargs['id'])
    # return HttpResponseRedirect(reverse('mapp:portfolio'))
    return render(request, 'mapp/handyman_portfolio.html',
                  {'handyman': CustomUser.objects.get(id=kwargs['id'])})


# View about the detail info of a assignment by both clients and handyman
def assigm_detail(request, **kwargs):
    # print("called for pro")
    # # print(kwargs['id'])
    return render(request, 'mapp/assignment_detail.html',
                  {'assignment': Assignment.objects.get(id=kwargs['id'])})


# View to delete a certain advertisment by handyamn
def delete_adv(request, **kwargs):
    if 'id' in kwargs.keys():
        obj = Advertisment.objects.get(pk=kwargs['id'])
        name = obj.title
        obj.delete()
        messages.warning(request, '"{}" was removed from Advertisments'.format(name))
    return redirect('mapp:handyman_adv')


# View to delete a certain assignment by client or a handyman
def delete_assigm(request, **kwargs):
    if 'id' in kwargs.keys():
        obj = Assignment.objects.get(pk=kwargs['id'])
        name = obj.__str__()
        messages.warning(request, '"{}" was removed from Assignments'.format(name))
    if request.user.is_handyman:
        return redirect('mapp:work')
    return redirect('mapp:assignments')


# View to edit the advertisment by author handyman
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


# View to post a new Advertisment by the handyman
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
    paginate_by = 5
    template_name = "mapp/home.html"

    def get_queryset(self):
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


'''
    This Advertisment Detail View, it has detail info about the advertisment and also contains the
    facility to book the advertised services by the user
'''


def get_available_dates(handyman_obj):
    india = pytz.timezone('Asia/Kolkata')
    current = india.localize(datetime.now())
    # current_hour = int(current.strftime('%H'))

    booked_dates = [india.normalize(d.date) for d in handyman_obj.dates_booked.all() if
                    india.normalize(d.date) > current]
    available_dates = []

    if current.hour < 7:
        start_date = india.localize(datetime(year=current.year, month=current.month, day=current.day, hour=9))
        ctr = 0
        while True:
            if start_date not in booked_dates:
                available_dates.append(start_date)
                break
            if ctr % 2 == 0:
                start_date += timedelta(hours=5)
            else:
                start_date += timedelta(hours=19)
            ctr += 1

        for i in range(9):
            if (ctr + i) % 2 == 0:
                start_date += timedelta(hours=5)
            else:
                start_date += timedelta(hours=19)
            if start_date not in booked_dates: available_dates.append(start_date)



    elif current.hour < 12:
        start_date = india.localize(datetime(year=current.year, month=current.month, day=current.day, hour=14))
        ctr = 0
        while True:
            if start_date not in booked_dates:
                available_dates.append(start_date)
                break
            if ctr % 2 != 0:
                start_date += timedelta(hours=5)
            else:
                start_date += timedelta(hours=19)
            ctr += 1

        for i in range(6):
            if (ctr + i) % 2 != 0:
                start_date += timedelta(hours=5)
            else:
                start_date += timedelta(hours=19)
            if start_date not in booked_dates: available_dates.append(start_date)


    else:
        start_date = india.localize(
            datetime(year=current.year, month=current.month, day=current.day, hour=9) + timedelta(days=1))
        ctr = 0
        while True:
            if start_date not in booked_dates:
                available_dates.append(start_date)
                break
            if ctr % 2 == 0:
                start_date += timedelta(hours=5)
            else:
                start_date += timedelta(hours=19)
            ctr += 1

        for i in range(9):
            if (ctr + i) % 2 == 0:
                start_date += timedelta(hours=5)
            else:
                start_date += timedelta(hours=19)
            if start_date not in booked_dates: available_dates.append(start_date)

    return available_dates


class AdvertismentDetailView(FormMixin, DetailView):
    model = Advertisment
    template_name = "mapp/detail.html"
    form_class = BookForm

    # def bookd_adv(self):
    #     print("Book")

    def get_context_data(self, **kwargs):
        # print(self.request.GET)
        # print('got here################################################################')
        # Call the base implementation first to get a context
        context = super(AdvertismentDetailView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        context['extra'] = context['advertisment'].services.all()
        context['form'] = BookForm(
            initial={'post': self.object, 'available_dates': get_available_dates(self.object.handyman)})

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
            appointment_date = datetime.strptime(post_data.get('appointment_date')[0], '%A, %dth %b %Y at %I:00 %p')

            services = post_data.get('services')
            if not services:
                messages.warning(request, f"Please Select on of the services")
                return self.render_to_response(self.get_context_data(form=form))

            adv_obj = self.object
            # datetime.strptime('02/04/2020 12:20', '%d/%m/%Y %H:%M')
            services_obj = [adv_obj.services.get(nameSlug=service_slug) for service_slug in services]

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

            date_obj = Dates(date=datetime.strptime(post_data.get('appointment_date')[0], '%A, %dth %b %Y at %I:00 %p'),
                             assignment_id=new_assignment_obj)
            date_obj.save()
            adv_obj.handyman.dates_booked.add(date_obj)

            messages.success(request, f"{adv_obj.title} has been booked.")

        if form.is_valid():
            cprint('Valid Form', 'green')
            return self.form_valid(form)
        else:
            cprint('Invalid Form', 'blue')
            return self.form_valid(form)
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# View to show all the Assignment for the client user
class AssignmentView(ListView):
    template_name = "mapp/assignments.html"
    model = Assignment

    def get_queryset(self):
        return Assignment.objects.filter(client=self.request.user)


# View to show all the Assignment for the handyman user
class WorkView(ListView):
    template_name = "mapp/work.html"
    model = Assignment

    def get_queryset(self):
        return Assignment.objects.filter(handyman=self.request.user)


# View to show all the Advertisment for the handyman
class HandymanAdvView(ListView):
    template_name = "mapp/handyman_adv_list.html"
    model = Advertisment

    def get_queryset(self):
        return Advertisment.objects.filter(handyman=self.request.user)


@login_required
def unbook(request, id):
    print("Unbook")
    adv = Assignment.objects.get(advertisment_id=id, client=request.user)
    title = adv.advertisment_id.title
    adv.delete()
    messages.warning(request, f"{title} has been unbooked.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ))
