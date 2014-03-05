from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')
    # Get BO
    
    cp = mmod.CatalogInventory.objects.get(id=request.urlparams[0])
    cp.active=False
    cp.save()

    return HttpResponseRedirect('/manager/productlist/')

# class StoreForm(forms.Form):
#   '''The store edit form'''
#   name = forms.CharField()
#   location = forms.CharField()
#   street = forms.CharField()
#   city = forms.CharField()
#   state = forms.CharField()
#   zipCode = forms.CharField()
#   phone = forms.CharField()
#   active = forms.BooleanField(required=False)