from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime


def process_request(request):
    '''Sends an employee to the form for updating labor information on a repair'''
    #Checks for an Authenticated User
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    if not request.user.is_staff:
       return HttpResponse('/homepage/')

    #Gets the user BO
    user = request.user
    sr = mmod.ServiceRepair.objects.get(id=request.urlparams[0])
    form = RepairWorkForm()
    now = datetime.now()


    if request.method == 'POST':
        form = RepairWorkForm(request.POST)
        if form.is_valid():
            work_performed = form.cleaned_data['work_performed']
            status = form.cleaned_data['status']
            hours_worked = form.cleaned_data['hours_worked']

            # charge_amount = form.cleaned_data['charge_amount']
            if status == 'Finished':
                sr.dateComplete = now

            sr.status = status
            sr.labor_hours += hours_worked
            sr.save()

        return HttpResponseRedirect('/manager/repair_details/')


    template_vars = {
        'user': user,
        'sr': sr,
        'form': form,

    }

    return templater.render_to_response(request, 'repair_work.html', template_vars)

class RepairWorkForm(forms.Form):
    '''The repair work form is used for employees to describe the labor performed during a repair'''    
    status = forms.ChoiceField(widget = forms.Select(), choices = ([('Waiting for Parts','Waiting for Parts'), ('On Hold','On Hold'),('In Progress','In Progress'),('Finished','Finished'), ]))   
    hours_worked = forms.IntegerField()
    work_performed = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'id':'laborBox','placeholder':'Description of labor performed'}))