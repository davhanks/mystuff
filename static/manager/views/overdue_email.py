from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
import datetime
from django.utils import timezone
from django.core.mail import send_mass_mail



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

    email_one = []
    email_two = []
    email_three = []

    for rent in one_month:
        for u in users:
            if u.id == rent.user_id:
                email_one.append(u.email)

    for rent in two_months:
        for u in users:
            if u.id == rent.user_id:
                email_two.append(u.email)

    for rent in three_months:
        for u in users:
            if u.id == rent.user_id:
                email_three.append(u.email)

    message1 = ('MyStuff Overdue Rental', 'Your rental is overdue. Please return it as soon as possible to avoid higher fees!', 'davidkhanks@gmail.com', email_one)
    message2 = ('MyStuff Overdue Rental', 'Your rental is more than 30 days overdue. Please return it as soon as possible to avoid higher fees!', 'davidkhanks@gmail.com', email_two)
    message3 = ('MyStuff Overdue Rental', 'Your rental is more than 60 days overdue. Please return it as soon as possible to avoid higher fees!', 'davidkhanks@gmail.com', email_three)

    send_mass_mail((message1, message2, message3), fail_silently=False)

    return HttpResponseRedirect('/manager/overdue_rentals/')
