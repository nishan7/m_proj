from crispy_forms.layout import Submit, Field, MultiField, Row, Column
from django import forms
# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget
from crispy_forms.helper import FormHelper
from django.forms import TypedMultipleChoiceField, formset_factory, inlineformset_factory

from .models import Advertisment, Service

# PAYMENT_CHOICES = (
#     ('S', 'Stripe'),
#     ('P', 'PayPal')
# )
# from django.forms import DateInput
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
# from datetimepicker.widgets import DateTimePicker
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div


class ServiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_serviceForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        if kwargs != {} and kwargs['initial'] != {}:
            # print(kwargs['initial']['post'].getServices(), '**')
            self.fields['services'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
            self.fields['services'].choices = [(s.nameSlug, s) for s in kwargs['initial']['post'].getServices()]

    # a = forms.CharField(required=False)
    # choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    appointment_date = forms.DateField(
        widget=(forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'placeholder': 'dd/mm/YYYY HH:MM'})))
    services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    address = forms.CharField(max_length=500)


class ServicePriceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServicePriceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_servicePriceForm'
        # self.helper.form_class = 'row'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.help_text_inline = True

        self.fields['name'] = forms.CharField(max_length=225, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name of Service'}))
        self.fields['price'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Price \u20B9'}))

    class Meta:
        model = Service
        fields = ('name', 'price')


service_formset = formset_factory(ServicePriceForm, extra=1)





class AdverstimentForm(forms.ModelForm):
    # name = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Enter Book Name here'
    #     })
    # )

    def __init__(self, *args, **kwargs):
        super(AdverstimentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_serviceForm'
        # self.helper.form_class = 'row'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.help_text_inline = True
        # self.helper.form_group_wrapper_class="wakaoo"
        self.helper.field_class = 'col-lg-8'
        self.helper.label_class = 'col-form-label col-sm-2'

        self.helper.layout = Layout(
            Div(
                Field('title', wrapper_class='form-group row'),
                # Field('handyman', wrapper_class='form-group row'),
                Field('image', wrapper_class='form-group row'),
                Field('task', wrapper_class='form-group row'),
                Field('category', wrapper_class='form-group row'),
                Field('description', wrapper_class='form-group row'),
                Field('ser', wrapper_class='form-group row'),
                # Field('service', wrapper_class='form-group row'),
            ),

        )

    class Meta:
        model = Advertisment
        fields = ['title', 'category', 'task', 'description', 'image']

# class AdverstimentForm(forms.ModelForm):
#     class Meta:
#         model= Advertisment
#         fields = ['title','price','handyman','task']
