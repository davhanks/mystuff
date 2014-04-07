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
    if request.user.is_staff:
        user = mmod.User.objects.get(id=request.urlparams[0])
    else:
        user = request.user
    sr = mmod.ServiceRepair.objects.filter(customer_id=user.id)
    now = timezone.now()
    status_list = ["Waiting for Parts","On Hold","In Progress","Finished"]
    


    template_vars = {
        'user': user,
        'sr': sr,
        'status_list': status_list,
    }

    return templater.render_to_response(request, 'check_status.html', template_vars)

