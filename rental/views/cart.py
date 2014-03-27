from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater



def process_request(request):
    cart = request.session.get('cart', {})
    products = []
    subtotal = 0

    for key in cart:
        prod = mmod.CatalogInventory.objects.get(id__in=key)
        products.append(prod)

        subtotal += (prod.sale_price * cart[key])



    template_vars = {
        'cart' : cart,
        'products' : products,
        'subtotal' : subtotal,
    }

    return templater.render_to_response(request, 'cart.html', template_vars)

def process_request__add(request):

    # get cart
    cart = request.session.get('cart', {})
    products = mmod.Product.objects.filter(catalog_inventory_id=request.urlparams[0]).filter(active=True)
    # if item exists in cart, add 1 else put item in cart with quantity of 1
    if len(products) > 0:
        if request.urlparams[0] in cart:
            if cart[request.urlparams[0]] == len(products):
                return HttpResponseRedirect('/catalog/stock/current/')
            else:
                cart[request.urlparams[0]] += 1
        else:
            cart[request.urlparams[0]] = 1
        request.session['cart'] = cart
        return HttpResponseRedirect('/catalog/list/all/')
    else:
        return HttpResponseRedirect('/catalog/stock/out/')


    return HttpResponseRedirect('/catalog/list/all/')

def process_request__remove(request):

    cart = request.session.get('cart', {})
    del cart[request.urlparams[0]]
    request.session['cart'] = cart

    return HttpResponseRedirect('/catalog/cart/')