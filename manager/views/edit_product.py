from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from datetime import datetime
from . import templater
import random


def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')


    error_code = 0
    error_mes = ''

    product = mmod.Product.objects.get(id=request.urlparams[0])

    form = EditProductForm(initial = {
        'shelf_location': product.shelf_location,

        })

    if request.method == 'POST':
        form = EditProductForm(request.POST)
        if form.is_valid():
            shelf = form.cleaned_data['shelf_location']

            product.shelf_location = shelf
            product.save()


            return HttpResponseRedirect('/manager/orderslist/')

    template_vars = {
        'form' : form,
    }

    return templater.render_to_response(request, 'edit_product.html', template_vars)



class EditProductForm(forms.Form):
    shelf_location = forms.CharField()

