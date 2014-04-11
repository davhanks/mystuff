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
        return HttpResponseRedirect('/manager/dashboard')
        
    products = mmod.CatalogInventory.objects.filter(active=True)

    template_vars = {
        'products': products,

    }

    return templater.render_to_response(request, 'productlist.html', template_vars)