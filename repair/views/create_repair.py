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
    customer = mmod.User.objects.get(id=request.urlparams[0])
    now = timezone.now()
    
    form = CreateRepairForm()


    if request.method == 'POST':
        form = CreateRepairForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            # charge_amount = form.cleaned_data['charge_amount']

            sr = mmod.ServiceRepair()
            sr.employee_id = user.id
            sr.customer_id = customer.id
            sr.dateStarted = now
            sr.description = description
            sr.status = status
            sr.save()


        return HttpResponseRedirect('/repair/userlookup/')


    template_vars = {
        'customer': customer,
        'user': user,
        'form': form,
    }

    return templater.render_to_response(request, 'create_repair.html', template_vars)

class CreateRepairForm(forms.Form):
    '''The Create a repair form'''
    description = forms.CharField(widget=forms.Textarea(attrs={'id':'damageBox','placeholder':'Description of problem'}))
    status = forms.ChoiceField(widget = forms.Select(), choices = ([('Waiting for parts','Waiting for parts'), ('On Hold','On Hold'),('In Progress','In Progress'),('Finished','Finished'), ]))   
