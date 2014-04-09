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
    sr = mmod.ServiceRepair.objects.filter(customer_id=user.id).exclude(picked_up=True)
    now = datetime.now()
    status_list = ["Waiting for Parts","On Hold","In Progress","Finished"]

    form = StatusForm()


    if request.method == 'POST':
        sr = mmod.ServiceRepair.objects.get(id=request.urlparams[1])
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['change_status']
            # hours_worked = form.cleaned_data['hours_worked']

            # charge_amount = form.cleaned_data['charge_amount']
            if status == 'Finished':
                sr.dateComplete = now

            sr.status = status
            # sr.labor_hours += hours_worked
            sr.save()


        return HttpResponseRedirect('/repair/check_status/' + request.urlparams[0] + '/')


    template_vars = {
        'user': user,
        'sr': sr,
        'status_list': status_list,
        'form': form,
    }

    return templater.render_to_response(request, 'check_status.html', template_vars)

class StatusForm(forms.Form):
    '''The Create a repair form'''
    change_status = forms.ChoiceField(widget = forms.Select(), choices = ([('Waiting for Parts','Waiting for Parts'), ('On Hold','On Hold'),('In Progress','In Progress'),('Finished','Finished'), ]))   
    # hours_worked = forms.IntegerField()