from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Show the product catalog in the db'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')

        
    products = mmod.Product.objects.all()
    stores = mmod.Store.objects.all()

    template_vars = {
        'products': products,
        'stores': stores,

    }

    return templater.render_to_response(request, 'rent.html', template_vars)