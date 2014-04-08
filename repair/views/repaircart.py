from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater



def process_request(request):
    repaircart = request.session.get('repaircart', {})
    catalog = mmod.CatalogInventory.objects.all()
    repairs = []
    user = mmod.User.objects.get(id=request.urlparams[0])

    for key in repaircart:
        if repaircart[key] == user.id:
            sr = mmod.ServiceRepair.objects.get(id=key)
            repairs.append(sr)


    template_vars = {
        'repaircart' : repaircart,
        'repairs': repairs,
        'user': user,

    }

    return templater.render_to_response(request, 'repaircart.html', template_vars)

def process_request__add(request):

    # get cart
    repaircart = request.session.get('repaircart', {})

    if request.urlparams[1] == 'all':
        return HttpResponseRedirect('/repair/stuff/')

    sr = mmod.ServiceRepair.objects.get(id=request.urlparams[1])

    print(str(sr.id) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    # if item exists in cart, add 1 else put item in cart with quantity of 1
    for key in repaircart:
        if key == str(sr.id):
            print("*******************" + str(sr.id))
            print("<<<<<<<<<<<<<<<<<<Already in cart")
            return HttpResponseRedirect('/repair/userlookup/')
    


    repaircart[str(sr.id)] = sr.customer_id
    request.session['repaircart'] = repaircart
    for key in repaircart:
        print("key: " + key + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Value: " + str(repaircart[key]) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


    return HttpResponseRedirect('/repair/userlookup/')

def process_request__remove(request):

    repaircart = request.session.get('repaircart', {})
    del repaircart[request.urlparams[0]]
    request.session['repaircart'] = repaircart

    return HttpResponseRedirect('/catalog/repaircart/')