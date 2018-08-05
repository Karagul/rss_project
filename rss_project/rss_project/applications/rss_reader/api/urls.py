from django.conf.urls import url

from .views import CurrencyConverterView

urlpatterns = [
    url(r'api/currency/list', CurrencyConverterView.as_view(), name='currency-all')
]
