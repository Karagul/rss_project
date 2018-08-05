from time import mktime

import feedparser
from celery import shared_task
from django.utils import timezone

from .models import Currency

RSS_COROUNCIES_LIST = [
        'https://www.ecb.europa.eu/rss/fxref-usd.html',
        'https://www.ecb.europa.eu/rss/fxref-jpy.html',
        'https://www.ecb.europa.eu/rss/fxref-bgn.html',
        'https://www.ecb.europa.eu/rss/fxref-czk.html',
        'https://www.ecb.europa.eu/rss/fxref-dkk.html',
        'https://www.ecb.europa.eu/rss/fxref-ekk.html',
        'https://www.ecb.europa.eu/rss/fxref-gbp.html',
        'https://www.ecb.europa.eu/rss/fxref-huf.html',
        'https://www.ecb.europa.eu/rss/fxref-pln.html',
        'https://www.ecb.europa.eu/rss/fxref-ron.html',
        'https://www.ecb.europa.eu/rss/fxref-sek.html',
        'https://www.ecb.europa.eu/rss/fxref-chf.html',
        'https://www.ecb.europa.eu/rss/fxref-isk.html',
        'https://www.ecb.europa.eu/rss/fxref-nok.html',
        'https://www.ecb.europa.eu/rss/fxref-hrk.html',
        'https://www.ecb.europa.eu/rss/fxref-rub.html',
        'https://www.ecb.europa.eu/rss/fxref-try.html',
        'https://www.ecb.europa.eu/rss/fxref-aud.html',
        'https://www.ecb.europa.eu/rss/fxref-brl.html',
        'https://www.ecb.europa.eu/rss/fxref-cad.html',
        'https://www.ecb.europa.eu/rss/fxref-cny.html',
        'https://www.ecb.europa.eu/rss/fxref-hkd.html',
        'https://www.ecb.europa.eu/rss/fxref-idr.html',
        'https://www.ecb.europa.eu/rss/fxref-inr.html',
        'https://www.ecb.europa.eu/rss/fxref-krw.html',
        'https://www.ecb.europa.eu/rss/fxref-mxn.html',
        'https://www.ecb.europa.eu/rss/fxref-myr.html',
        'https://www.ecb.europa.eu/rss/fxref-nzd.html',
        'https://www.ecb.europa.eu/rss/fxref-php.html',
        'https://www.ecb.europa.eu/rss/fxref-sgd.html',
        'https://www.ecb.europa.eu/rss/fxref-thb.html',
        'https://www.ecb.europa.eu/rss/fxref-zar.html',
    ]


@shared_task
def read_currencies():
    for link in RSS_COROUNCIES_LIST:
        read_currency.s(link=link).delay()


@shared_task
def read_currency(link):
    currency_data = feedparser.parse(link)
    for feed in currency_data['entries']:
        how_much_for_euro = feed.cb_exchangerate
        how_much_for_euro = how_much_for_euro.split('\n')[0]
        currency = feed.cb_targetcurrency
        date = feed.updated_parsed
        date = timezone.datetime.fromtimestamp(mktime(date))
        Currency.objects.get_or_create(value=how_much_for_euro, name=currency, created=date)
