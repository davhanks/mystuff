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
        
    users = mmod.User.objects.filter(is_active=True)
    #print(">>>>>>>>>>>>>>", stores)

    template_vars = {
        'users': users,

    }

    return templater.render_to_response(request, 'userlist.html', template_vars)