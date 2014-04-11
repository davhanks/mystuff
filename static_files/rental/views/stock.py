from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''
    if request.urlparams[0] == 'out':
        message = "We're sorry but this item is temporarily out of stock."
    else:
        message = "You have every available item of this type already in your cart."



    template_vars = {
        'message': message,
    }

    return templater.render_to_response(request, 'stock.html', template_vars)