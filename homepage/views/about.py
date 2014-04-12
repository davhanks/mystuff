from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''

    stores = mmod.Store.objects.all()



    template_vars = {
        'stores': stores,
    }

    return templater.render_to_response(request, 'about.html', template_vars)