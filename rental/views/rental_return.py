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
    products = mmod.Product.objects.all()
    rental = mmod.Rental.objects.get(id=request.urlparams[0])
    rental_items = mmod.RentalItem.objects.filter(rental_id=rental.id)

    time = timezone.now()
    now = time



    template_vars = {
        'user': user,
        'catalog': catalog,
        'products': products,
        'rental': rental,
        'now': now,
        'rental_items': rental_items,

    }

    return templater.render_to_response(request, 'rental_return.html', template_vars)
