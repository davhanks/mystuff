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
    # Get BO
    if request.urlparams[0] == 'new':
        s = mmod.Store()
        s.name = 'New Store'
        s.active = True
        s.save()
        return HttpResponseRedirect('/manager/editstore/' + str(s.id))
    else:
        s = mmod.Store.objects.get(id=request.urlparams[0])

    # run the form
    form = StoreForm(initial={

        'name': s.name,
        'location': s.location,
        'street': s.street,
        'city': s.city,
        'state': s.state,
        'zipCode': s.zipCode,
        'phone': s.phone,
    })
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            s.name = form.cleaned_data['name']
            s.location = form.cleaned_data['location']
            s.street = form.cleaned_data['street']
            s.city = form.cleaned_data['city']
            s.state = form.cleaned_data['state']
            s.zipCode = form.cleaned_data['zipCode']
            s.phone = form.cleaned_data['phone']
            s.save()
            return HttpResponseRedirect('/manager/storelist/')

    template_vars = {
        'form': form,
        'id': s.id,

    }

    return templater.render_to_response(request, 'editstore.html', template_vars)

class StoreForm(forms.Form):
    '''The store edit form'''
    name = forms.CharField()
    location = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    phone = forms.CharField()
