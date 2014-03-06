from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''
    if request.urlparams[0] == 'all':
        products = mmod.CatalogInventory.objects.all()
    else:
        products = mmod.CatalogInventory.objects.filter(product_category=request.urlparams[0])



    template_vars = {
        'products': products,

    }

    return templater.render_to_response(request, 'list.html', template_vars)