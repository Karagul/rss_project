from django.db import models


class Currency(models.Model):
    value = models.DecimalField(decimal_places=7, max_digits=10)
    name = models.CharField(max_length=3)
    created = models.DateTimeField()
