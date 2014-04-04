from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
import datetime
from django.utils import timezone



def process_request(request):
    '''Get products from the DB'''
    catalog = mmod.CatalogInventory.objects.all()
    users = mmod.User.objects.all()
    # now = datetime.datetime.now()

    time = timezone.now()

    now = time

    users = mmod.User.objects.all()

    one_month_ago = now - datetime.timedelta(days=30)
    two_months_ago = now - datetime.timedelta(days=60)
    three_months_ago = now - datetime.timedelta(days=90)

    one_month = mmod.Rental.objects.filter(dateDue__gte=one_month_ago, dateDue__lte=now).exclude(returned=True) 
    two_months = mmod.Rental.objects.filter(dateDue__gte=two_months_ago, dateDue__lte=one_month_ago).exclude(returned=True)
    three_months = mmod.Rental.objects.filter(dateDue__lte=two_months_ago).exclude(returned=True)

    length_one = len(one_month)
    length_two = len(two_months)
    length_three = len(three_months)

    if length_one == 0:
        length_one = 0

    if length_two == 0:
        length_two = 0

    if length_three == 0:
        length_three = 0

    print(length_three)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


    template_vars = {
        'users': users,
        'length_one': length_one,
        'length_two': length_two,
        'length_three': length_three,
        'one_month': one_month,
        'two_months': two_months,
        'three_months': three_months,
        'catalog': catalog,
        'users': users,
    }

    return templater.render_to_response(request, 'overdue_rentals.html', template_vars)



