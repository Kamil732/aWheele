from django.urls import path, include
from django.views.generic import TemplateView
# from django.views.decorators.cache import cache_page
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'products'
urlpatterns = (
    path('', views.PromoListView.as_view(), name='promo-list'),
    path('get-city-location', views.GetCityLocation.as_view(), name='get-city-location'),
    path(_('offers/'), include([
        path('get-average-price/<slug:product_class>', views.GetAveragePrice.as_view(), name='get-average-price'),
        path(_('search'), views.SearchProductView.as_view(), name='search'),
        path(_('observed/'), include([
            path('', views.ObservedProductsView.as_view(), name='observed-offers'),
            path(_('transport'), views.TransportObservedProducts.as_view(), name='transport-observed-offers'),
            path('<slug:section>/<int:product_id>/', include([
                path(_('add'), views.AddObservedProduct.as_view(), name='add-observed-offer'),
                path(_('remove'), views.RemoveObservedProduct.as_view(), name='remove-observed-offer'),
            ])),
        ])),
        path(_('create/'), include([
            path('', TemplateView.as_view(template_name='products/kind_of_product_to_create.html'), name='kind-of-offer-to-create'),
            path('<slug:section>', login_required(views.CreateProductView.as_view()), name='create-product')
        ])),
        path(_('delete-product/<slug:product_class>/<int:product_id>'), login_required(views.DeleteProduct.as_view()), name='delete-product'),
        path('<slug:section>/<slug:product_slug>/', include([
            path('', views.DetailView.as_view(), name='detail'),
            path('show-phonenumber', views.ShowPhonenumber.as_view(), name='show-phonenumber'),
            path(_('send-email'), views.SendEmail.as_view(), name='send-email'),
        ])),
    ])),
)