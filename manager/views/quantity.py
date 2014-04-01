from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from datetime import datetime
from . import templater
import random


def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')

    #Error code logic is copied from another py file and is commented out to allow
    #for future error handling. Plans to allow the choice of how many to order at a time
    #are in the works and this style of error codes will help to mitigate problems
    # later on.

    error_code = 0
    error_mes = ''
    catalogid = request.urlparams[1]
    storeid = request.urlparams[0]

    # form = QuantityForm(initial = {
    #     'quantity': 1,


    #     })

    # if request.method == 'POST':
    #     form = QuantityForm(request.POST)
    #     if form.is_valid():
    #         quantity = form.cleaned_data['quantity']


            # if password != retype:
            #     error_code = 2
            # for u in users:
            #     if u.username == username:
            #         error_code = 1
            #         break

    if error_code == 1:
        error_mes = 'This username is already in use'
    elif error_code == 2:
        error_mes = 'Passwords must match'
    
    if error_code == 0:
    
        u = mmod.Product()
        u.catalog_inventory_id = catalogid
        u.store_id = storeid
        u.shelf_location = 'Storage Room'
        u.purchase_date = datetime.now().date()
        u.serial_number = random.randrange(1000,99999)
        u.active = True
        u.is_rental = False
        u.save()

    return HttpResponseRedirect('/manager/productlist/')