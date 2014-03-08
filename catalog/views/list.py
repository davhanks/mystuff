from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''
    if request.urlparams[0] == 'all':
        products = mmod.CatalogInventory.objects.filter(active=True)
    else:
        products = mmod.CatalogInventory.objects.filter(product_category=request.urlparams[0])



    template_vars = {
        'products': products,
    }

    return templater.render_to_response(request, 'list.html', template_vars)



def process_request__search(request):
    try:
        products = mmod.CatalogInventory.objects.filter(product_category__icontains=request.POST.get('search', ''))
    except CatalogInventory.DoesNotExist:
        products = mmod.CatalogInventory.ojects.none()

    if len(products)==0:
        try:
            products = mmod.CatalogInventory.objects.filter(product_name__icontains=request.POST.get('search',''))
        except CatalogInventory.DoesNotExist:
            products = mmod.CatalogInventory.objects.none()

    if len(products)==0:
        try:
            products = mmod.CatalogInventory.objects.filter(manufacturer__icontains=request.POST.get('search',''))
        except CatalogInventory.DoesNotExist:
            products = mmod.CatalogInventory.objects.none()

    if len(products)==0:
        try:
            products = mmod.CatalogInventory.objects.filter(description__icontains=request.POST.get('search',''))
        except CatalogInventory.DoesNotExist:
            products = mmod.CatalogInventory.objects.none()

    template_vars = {
        'products': products,
    }

    return templater.render_to_response(request, 'list.html', template_vars)