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
    else:
        return HttpResponseRedirect('/catalog/list/all/')



    template_vars = {
        'product': product,
    }

    return templater.render_to_response(request, 'description.html', template_vars)