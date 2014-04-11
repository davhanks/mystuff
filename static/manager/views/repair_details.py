from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Sends user to the dashboard'''

    

    #Checks for an Authenticated User
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
       return HttpResponse('/homepage/')

    #Gets the user BO in order to pass information
    user = request.user

    finished_repairs = mmod.ServiceRepair.objects.exclude(picked_up=True).filter(status='Finished')
    repairs = mmod.ServiceRepair.objects.exclude(picked_up=True).exclude(status='Finished')
    num_repairs = len(repairs)


    template_vars = {
        'user': user,
        'repairs': repairs,
        'finished_repairs': finished_repairs,
        'num_repairs': num_repairs,
    }

    return templater.render_to_response(request, 'repair_details.html', template_vars)