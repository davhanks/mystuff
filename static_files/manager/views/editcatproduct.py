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
        return HttpResponseRedirect('/account/accountDashboard/')
    # Get BO
    if request.urlparams[0] == 'new':
        cp = mmod.CatalogInventory()
        # cp.product_name = 'New Product'
        cp.active = True
        cp.save()
        return HttpResponseRedirect('/manager/editcatproduct/' + str(cp.id))
    else:
        cp = mmod.CatalogInventory.objects.get(id=request.urlparams[0])

    # run the form
    form = CatProductForm(initial={

        'product_name': cp.product_name,
        'description': cp.description,
        'manufacturer': cp.manufacturer,
        'average_cost': cp.average_cost,
        'sale_price' : cp.sale_price,
        'commission_rate': cp.commission_rate,
        'product_category': cp.product_category,
        'sku': cp.sku,
        'image_name': cp.image,
    })
    if request.method == 'POST':
        form = CatProductForm(request.POST)
        if form.is_valid():
            cp.product_name = form.cleaned_data['product_name']
            cp.description = form.cleaned_data['description']
            cp.manufacturer = form.cleaned_data['manufacturer']
            cp.average_cost = form.cleaned_data['average_cost']
            cp.sale_price = form.cleaned_data['sale_price']
            cp.commission_rate = form.cleaned_data['commission_rate']
            cp.product_category = form.cleaned_data['product_category']
            cp.sku = form.cleaned_data['sku']
            cp.image = form.cleaned_data['image_name']
            cp.save()
            return HttpResponseRedirect('/manager/productlist/')

    template_vars = {
        'form': form,
        'id': cp.id,

    }

    return templater.render_to_response(request, 'editcatproduct.html', template_vars)

class CatProductForm(forms.Form):
    '''The CatalogInventory edit form'''
    product_name = forms.CharField()
    description = forms.CharField()
    manufacturer = forms.CharField()
    average_cost = forms.DecimalField()
    sale_price = forms.DecimalField()
    commission_rate = forms.DecimalField()
    product_category = forms.CharField()
    sku = forms.IntegerField()
    image_name = forms.CharField()