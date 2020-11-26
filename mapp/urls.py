from django.urls import path

from . import views
from .views import *

# TODO search for categories,
app_name = 'mapp'

urlpatterns = (

    path('', HomeView.as_view(), name='home'),
    path('<category>', HomeView.as_view(), name='category-home'),
    path('detail/<slug>', AdvertismentDetailView.as_view(), name='detail'),
    path('unbook/<id>', views.unbook, name='unbook'),
    path('assignment/', AssignmentView.as_view(), name='assignments'),
    path('work/', WorkView.as_view(), name='work'),
    path('portfolio/<id>', views.portfolioView, name='portfolio'),
    path('assigm_detail/<id>', views.assigm_detail, name='assigm_detail'),
    path('advertisment_form/',views.adv_view, name='advertisment_form'),
    path('advertisment_form/<id>',views.adv_edit_view, name='advertisment_form_edit'),
    path('delete/<id>',views.delete_adv, name='delete_adv'),
    path('delete_assigm/<id>',views.delete_assigm, name='delete_assigm'),
    path('handyman_adv/',HandymanAdvView.as_view(), name='handyman_adv'),
    path('chat/<user_id>',views.chat, name='chat'),

)
