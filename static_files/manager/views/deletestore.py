from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')
    # Get BO
    
    s = mmod.Store.objects.get(id=request.urlparams[0])
    s.active=False
    s.save()

    return HttpResponseRedirect('/manager/storelist/')