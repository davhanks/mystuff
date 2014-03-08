from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater



def process_request(request):
    cart = request.session.get('cart', {})
    products = []

    for key in cart:
        prod = mmod.CatalogInventory.objects.get(id__in=key)
        products.append(prod)


    template_vars = {
        'cart' : cart,
        'products' : products,
    }

    return templater.render_to_response(request, 'cart.html', template_vars)

def process_request__add(request):

    # get cart
    cart = request.session.get('cart', {})

    # if item exists in cart, add 1 else put item in cart with quantity of 1
    if request.urlparams[0] in cart:
        cart[request.urlparams[0]] += 1
    else:
        cart[request.urlparams[0]] = 1
    request.session['cart'] = cart



    return HttpResponseRedirect('/catalog/list/all/')

def process_request__remove(request):

    cart = request.session.get('cart', {})
    del cart[request.urlparams[0]]
    request.session['cart'] = cart

    return HttpResponseRedirect('/catalog/cart/')