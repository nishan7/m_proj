from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views
from .views import *

# TODO search for categories,
app_name = 'mapp'

urlpatterns = (
    # path('', views.index, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('<category>', HomeView.as_view(), name='category-home'),
    # path('', HomeView.as_view(), name='search-home'),
    path('detail/<slug>', AdvertismentDetailView.as_view(), name='detail'),
    # path('search/<query>', HomeView.as_view(), name='search'),
    path('book/<slug>', views.book, name='book'),
    path('unbook/<id>', views.unbook, name='unbook'),
    path('assignment/', AssignmentView.as_view(), name='assignments'),
    path('work/', WorkView.as_view(), name='work'),
    path('portfolio/<id>', views.portfolioView, name='portfolio'),
    path('advertisment_form/',views.adv_view, name='advertisment_form'),
    path('advertisment_form/<id>',views.adv_edit_view, name='advertisment_form_edit'),
    path('handyman_adv/',HandymanAdvView.as_view(), name='handyman_adv'),
    # path('advertisment_form/', AdvertismentFormView.as_view(), name='advertisment_form'),

    # path('items/', HomeView.as_view(), name="item_list"),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    # path('remove-from-cart/<slug>', remove_from_cart, name="remove-from-cart"),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('payment/', PaymentView.as_view(), name='payment'),
    # path('info/', views.info, name='info'),
    # path('register/', views.register, name='register'),
    # path('logout/', views.user_logout, name='logout'),
    # path('login/', views.user_login, name='login')
)
