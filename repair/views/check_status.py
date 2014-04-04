from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
from django.utils import timezone



def process_request(request):
    '''Get products from the DB'''
    user = request.user
    sr = mmod.ServiceRepair.objects.filter(id=user.id)
    now = timezone.now()
    



    


    template_vars = {
        'user': user,
        'sr': sr,
    }

    return templater.render_to_response(request, 'check_status.html', template_vars)

