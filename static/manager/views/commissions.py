from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
from datetime import timedelta
from random import randint


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')


    employees = mmod.User.objects.filter(is_staff=True)

    now = datetime.now()
    begin = now - timedelta(days=30)

    commissions = mmod.Commission.objects.all()
    # filter(date__gte=begin, date__lte=now)

  

    template_vars = {
        'employees': employees,
        'commissions': commissions,
    }

    return templater.render_to_response(request, 'commissions.html', template_vars)