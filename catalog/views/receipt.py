from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
from random import randint


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')

    sale = mmod.Sale.objects.get(id=request.session['sale_id'])
    saleItems = mmod.SaleItem.objects.filter(sale_id=sale.id)

  

    template_vars = {
        'sale': sale,
    }

    return templater.render_to_response(request, 'receipt.html', template_vars)