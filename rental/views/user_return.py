from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
from django.utils import timezone



def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[0])
    catalog = mmod.CatalogInventory.objects.all()
    products = mmod.Product.objects.all()
    rentals = mmod.Rental.objects.filter(user_id=user.id)
    now = timezone.now()

    return_items = []    

    for rent in rentals:
        rental_items = mmod.RentalItem.objects.filter(id=rent.id)
        for ri in rental_items:
            return_items.append(ri)
    




    template_vars = {
        'user': user,
        'rentals':rentals,
        'return_items': return_items,
        'catalog': catalog,
        'products': products,
        'now': now,
    }

    return templater.render_to_response(request, 'user_return.html', template_vars)



