from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .decorators import unautthenticated_user
from . import views

app_name = 'accounts'
urlpatterns = [
    path(_('login/'), unautthenticated_user(views.LoginView.as_view()), name='login'),
    path(_('register/'), unautthenticated_user(views.RegisterView.as_view()), name='register'),
    path(_('logout'), views.LogoutView.as_view(), name='logout'),
    path(_('my-offers/'), include([
        path(_('<slug:status>'), login_required(views.MyProducts.as_view()), name='my-products'),
    ])),
]