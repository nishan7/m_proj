from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    # path('logout/', views.LoggedOut.as_view(template_name="accounts/logged_out.html"), name='logout'),
    path('accounts/signup/', views.SignUp.as_view(template_name="accounts/signup.html"), name='signup'),
    path('', views.logged_out, name='logout'),

    # path('', views.logged_in, name='logged_in'),
    # path('', views.logged_out, name='logged_out'),

]
