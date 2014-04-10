from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Show the product catalog in the db'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard/')
        
    form = SortForm()
    products = mmod.Product.objects.all()
    stores = mmod.Store.objects.all()
    catalog = mmod.CatalogInventory.objects.all()


    template_vars = {
        'products': products,
        'stores': stores,
        'catalog': catalog,
        'form': form,

    }

    return templater.render_to_response(request, 'orderslist.html', template_vars)


def process_request__make_rental(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard/')

    form = SortForm()
    catalog = mmod.CatalogInventory.objects.all()
    products = mmod.Product.objects.all()
    stores = mmod.Store.objects.all()
    
    product = mmod.Product.objects.get(id=request.urlparams[0])
    if request.method == "POST":
        if product.active: 
            product.is_rental = True
            product.rented_out = False
            if product.times_rented == None:
                product.times_rented = 0

            if request.POST.get('amount') == '':
                product.rental_fee = 1
            else:
                product.rental_fee = request.POST.get('amount')

            product.save()
        

    template_vars = {
        'products': products,
        'stores': stores,
        'catalog': catalog,
        'form': form,
    }

    return templater.render_to_response(request, 'orderslist.html', template_vars)


def process_request__sort(request):
    '''Show the product catalog in the db'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard/')
        
    form = SortForm()
    stores = mmod.Store.objects.all()
    catalog = mmod.CatalogInventory.objects.all()

    if request.method == "POST":
        form = SortForm(request.POST)
        if form.is_valid():
            sort_by = form.cleaned_data['sort_by']
            ascending = form.cleaned_data['ascending']
            query = ''

            if ascending == True:
                query = sort_by
            else:
                query = '-' + sort_by

            products = mmod.Product.objects.order_by(query)

    template_vars = {
        'products': products,
        'stores': stores,
        'catalog': catalog,
        'form': form,

    }

    return templater.render_to_response(request, 'orderslist.html', template_vars)

class SortForm(forms.Form):
    '''The Create a repair form'''
    sort_by = forms.ChoiceField(label='', widget = forms.Select(), choices = ([('store','Store'), ('serial_number','Serial Number'),('active','Sold'),('purchase_date','Date'),('rental_fee','Fee'),('catalog_inventory','Catalog Product'), ('shelf_location','Shelf Location') ]))
    ascending = forms.NullBooleanField(label='', widget=forms.RadioSelect(choices=[(1, 'Ascending'),(0, 'Descending')]))
