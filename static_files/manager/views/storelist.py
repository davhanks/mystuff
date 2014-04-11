from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Show all stores in the db'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')
        
    stores = mmod.Store.objects.filter(active=True)
    #print(">>>>>>>>>>>>>>", stores)

    template_vars = {
        'stores': stores,

    }

    return templater.render_to_response(request, 'storelist.html', template_vars)