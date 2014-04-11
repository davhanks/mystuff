from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from django.contrib.auth import logout


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')

    # Get BO
    
    uid = request.user.id
    u = mmod.User.objects.get(id=uid)
    u.is_active=False
    u.save()
    logout(request)

    return HttpResponseRedirect('/homepage/')