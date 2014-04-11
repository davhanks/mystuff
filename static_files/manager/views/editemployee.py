from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')

    try:
        e = mmod.Employee.objects.get(user=request.urlparams[0])
    except mmod.Employee.objects.DoesNotExist:
        e = mmod.Employee()
        e.user=request.urlparams[0]

    # run the form
    form = EmployeeForm(initial={

        'hire_date': e.hire_date,
        'termination_date': e.termination_date,
        'salary': e.salary,
    })
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            e.hire_date = form.cleaned_data['username']
            e.termination_date = form.cleaned_data['first_name']
            e.salary = form.cleaned_data['last_name']
            return HttpResponseRedirect('/manager/employeelist/')

    template_vars = {
        'form': form,
        'id': e.id,

    }

    return templater.render_to_response(request, 'edituser.html', template_vars)

class employeeForm(forms.Form):
    '''The store edit form'''
    hire_date = forms.DateField()
    termination_date = forms.DateField(required=False)
    salary = forms.DecimalField(decimal_places=2)

