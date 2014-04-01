from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Show the product catalog in the db'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard/')
        
    products = mmod.Product.objects.all()
    stores = mmod.Store.objects.all()

    template_vars = {
        'products': products,
        'stores': stores,

    }

    return templater.render_to_response(request, 'orderslist.html', template_vars)


def process_request__make_rental(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard/')
    
    product = mmod.Product.objects.get(id=request.urlparams[0])
    if product.active: 
        product.is_rental = True
        product.rented_out = False
        product.times_rented = 0
        product.save()
    

    products = mmod.Product.objects.all()
    stores = mmod.Store.objects.all()

    template_vars = {
        'products': products,
        'stores': stores,
    }

    return templater.render_to_response(request, 'orderslist.html', template_vars)