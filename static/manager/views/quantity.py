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


    error_code = 0
    error_mes = ''
    catalogid = request.urlparams[1]
    storeid = request.urlparams[0]

    catProd = mmod.CatalogInventory.objects.get(id=catalogid)

    form = QuantityForm(initial = {
        'quantity': 1,


        })

    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print(quantity)

            for i in range(0, int(quantity)):
                print(i)
    
                u = mmod.Product()
                u.catalog_inventory_id = catalogid
                u.store_id = storeid
                u.shelf_location = 'Storage Room'
                u.purchase_date = datetime.now().date()
                u.serial_number = random.randrange(1000,99999)
                u.active = True
                u.is_rental = False
                u.save()

                ###############################################################
                revSrc = mmod.Loan()
                revSrc.amount = catProd.average_cost
                revSrc.note = 'Product Purchase'
                revSrc.save()

                journ = mmod.JournalEntry()
                journ.revenueSource_id = revSrc.id
                journ.save()

                # debit lta for amount of store
                ent = mmod.Debit()
                ent.GeneralLedgerName_id = 4
                ent.journalEntry_id = journ.id
                ent.amount = revSrc.amount
                ent.save()

                # credit cash for amount of store
                ent = mmod.Credit()
                ent.GeneralLedgerName_id = 1
                ent.journalEntry_id = journ.id
                ent.amount = revSrc.amount
                ent.save()
                # END

            return HttpResponseRedirect('/manager/productlist/')

    template_vars = {
        'form' : form,
    }

    return templater.render_to_response(request, 'quantity.html', template_vars)



class QuantityForm(forms.Form):
    quantity = forms.CharField(label="Quantity", required=True)

