from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import *
from django.utils import timezone



def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[1])
    catalog = mmod.CatalogInventory.objects.all()
    products = mmod.Product.objects.filter(rented_out=True)
    rental = mmod.Rental.objects.get(id=request.urlparams[0])
    rental_items = mmod.RentalItem.objects.filter(rental_id=rental.id)

    time = timezone.now()
    now = time

    late_fee = 0




    return_prods = []

    for ri in rental_items:
        for prod in products:
            if ri.product_id == prod.id:
                late_fee += prod.rental_fee
                return_prods.append(prod)

    for rp in return_prods:
        rp.rented_out = False
        rp.save()


    rental.dateIn = now
    if rental.dateIn > rental.dateDue:
        delta = rental.dateIn - rental.dateDue
        amount_days = delta.days

        amount_fee = late_fee * amount_days

        l = mmod.Late()
        l.amount = amount_fee
        l.rental_id = rental.id
        l.waived = False
        l.days_late = amount_days
        l.save()

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(amount_days)
        print(amount_fee)






    rental.returned = True
    rental.save()





    template_vars = {
        'user': user,
        'catalog': catalog,
        'products': products,
        'rental': rental,
        'now': now,
        'rental_items': rental_items,
        'return_prods': return_prods,

    }

    return templater.render_to_response(request, 'return_confirmation.html', template_vars)
