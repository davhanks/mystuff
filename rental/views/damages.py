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
    rental = mmod.Rental.objects.get(id=request.urlparams[0])
    user = mmod.User.objects.get(id=request.urlparams[1])
    product = mmod.Product.objects.get(id=request.urlparams[2])
    catalog = mmod.CatalogInventory.objects.get(id=product.catalog_inventory_id)
    ri = mmod.RentalItem.objects.get(rental_id=rental.id, product_id=product.id)
    
    form = DamageForm()


    if request.method == 'POST':
        form = DamageForm(request.POST)
        if form.is_valid():
            damage = form.cleaned_data['damages']

            charge_amount = form.cleaned_data['charge_amount']

            d = mmod.Damage()
            d.rental_id = rental.id
            d.waived = False
            d.description = damage
            d.product_id = product.id
            d.amount = charge_amount
            d.save()

            ri.damage_reported = True
            ri.save()

        return HttpResponseRedirect('/rental/rental_return/' + str(rental.id) + '/' + str(user.id) + '/')


    template_vars = {
        'rental':rental,
        'user': user,
        'product': product,
        'catalog': catalog,
        'form': form,
    }

    return templater.render_to_response(request, 'damages.html', template_vars)

class DamageForm(forms.Form):
    '''The damages form'''
    damages = forms.CharField(widget=forms.Textarea(attrs={'id':'damageBox','placeholder':'Damages'}))
    charge_amount = forms.DecimalField(max_digits=15, decimal_places=2)
