from django.views.generic import TemplateView


class TestPage(TemplateView):
    template_name = 'products/../accounts/templates/accounts/logged_in.html'


class ThanksPage(TemplateView):
    template_name = 'products/../accounts/templates/accounts/logged_out.html'


class HomePage(TemplateView):
    template_name = "mapp/home.html"
