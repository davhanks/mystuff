from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
import datetime
from django.utils import timezone
from django.core.mail import send_mail



def process_request(request):
    '''Get products from the DB'''
    catalog = mmod.CatalogInventory.objects.all()
    users = mmod.User.objects.all()


    finished_repairs = mmod.ServiceRepair.objects.exclude(picked_up=True).filter(status='Finished')


    email_one = []


    for r in finished_repairs:
        for u in users:
            if u.id == r.customer_id:
                email_one.append(u.email)


    send_mail('DigitalMyWorld Repair Complete', 'Your repair is complete. Come by to pick it up within the next 7 days!', 'davidkhanks@gmail.com', email_one, fail_silently=False)
   


    return HttpResponseRedirect('/manager/repair_details/')