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
    now = timezone.now()
    rental_items = mmod.RentalItem.objects.filter(rental_id=rental.id)

    late_fee = 5.00




    return_prods = []

    # for ri in rental_items:
    #     for prod in products:
    #         if ri.product_id == prod.id:
    #             return_prods.append(prod)

    # for rp in return_prods:
    #     rp.rented_out = False
    #     rp.save()


    rental.dateIn = now
    if rental.dateIn > rental.dateDue:
        delta = rental.dateIn - rental.dateDue
        amount_days = delta.days

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(amount_days)
        amount_days *=late_fee

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(amount_days)




    # rental.returned = True
    # rental.save()





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