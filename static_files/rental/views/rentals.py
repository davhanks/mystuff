from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater

def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    
    store = mmod.Store.objects.get(id=request.urlparams[0])
    catalog = mmod.CatalogInventory.objects.all()
    products = mmod.Product.objects.filter(is_rental=True).filter(store_id=store.id).filter(rented_out=False)
    stores = mmod.Store.objects.all()

    length = len(products)

    template_vars = {
        'catalog': catalog,
        'products': products,
        'stores': stores,
        'store': store,
        'length': length,
    }

    return templater.render_to_response(request, 'rentals.html', template_vars)