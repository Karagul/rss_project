from rest_framework import generics
from .serializers import CurrencySerializer
from ..models import Currency


class CurrencyConverterView(generics.ListAPIView):

    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.all()
