from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from random import randint
from datetime import datetime


def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.session['current_user'])
    number = request.session['rental']
    rental = mmod.Rental.objects.get(id=number)
    
    
    rentalcart = request.session.get('rentalcart', {})
    catalog = mmod.CatalogInventory.objects.all()
    products = []
    error_code = 0

    for key in rentalcart:
        prod = mmod.Product.objects.get(id=key)
        products.append(prod)

    form = TermsForm()

    request.session['rentalcart'] = {}


    template_vars = {
        'user': user,
        'form': form,
        'products': products,
        'catalog': catalog,
        'error_code': error_code,
        'rental': rental,
        'number': number,
    }

    return templater.render_to_response(request, 'rentalreceipt.html', template_vars)



  
class TermsForm(forms.Form):
    '''The Lookup form'''
    begin_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker formHeight', 'placeholder':'Begin Date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker formPad', 'placeholder':'End Date'}))
    rate_per_day = forms.DecimalField(widget=forms.TextInput(attrs={'id': 'rate', 'class':'formPad',  'placeholder':'Rate Per Day'}), decimal_places=2)
    
