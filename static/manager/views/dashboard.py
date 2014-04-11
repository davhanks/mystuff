from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Sends user to the dashboard'''

    #Gets the user BO in order to pass information
    u = request.user

    #Checks for an Authenticated User
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')


    template_vars = {
        'user': u,
    }

    return templater.render_to_response(request, 'dashboard.html', template_vars)