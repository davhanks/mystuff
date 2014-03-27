from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''
    if request.urlparams[0]:
        product = mmod.CatalogInventory.objects.get(id=request.urlparams[0])
        physicalProd = mmod.Product.objects.filter(catalog_inventory_id=request.urlparams[0]).filter(active=True)
    else:
        return HttpResponseRedirect('/catalog/list/all/')

    amount = len(physicalProd)


    template_vars = {
        'product': product,
        'amount' : amount,
    }

    return templater.render_to_response(request, 'description.html', template_vars)