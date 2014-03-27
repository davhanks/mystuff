from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater



def process_request(request):
    rentalcart = request.session.get('rentalcart', {})
    catalog = mmod.CatalogInventory.objects.all()
    products = []

    for key in rentalcart:
        prod = mmod.Product.objects.get(id=key)
        products.append(prod)


    template_vars = {
        'rentalcart' : rentalcart,
        'catalog': catalog,
        'products': products,

    }

    return templater.render_to_response(request, 'rentalcart.html', template_vars)

def process_request__add(request):

    # get cart
    rentalcart = request.session.get('rentalcart', {})
    product = mmod.Product.objects.get(id=request.urlparams[0])

    print(str(product.id) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    for key in rentalcart:
        if key == str(product.id):
            print("*******************" + str(product.id))
            print("<<<<<<<<<<<<<<<<<<Already in cart")
            return HttpResponseRedirect('/catalog/rentals/' + request.urlparams[1] + '/')
    # # if item exists in cart, add 1 else put item in cart with quantity of 1

    # if str(product.id) in rentalcart:
    #     print("<<<<<<<<<<<<<<<<<<Already in cart")
    #     return HttpResponseRedirect('/catalog/rentals/' + request.urlparams[1] + '/')
    # else:
    rentalcart[str(product.id)] = product.store_id
    request.session['rentalcart'] = rentalcart
    for key in rentalcart:
        print("key: " + key + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Value: " + str(rentalcart[key]) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


    return HttpResponseRedirect('/catalog/rent/')

def process_request__remove(request):

    rentalcart = request.session.get('rentalcart', {})
    del rentalcart[request.urlparams[0]]
    request.session['rentalcart'] = rentalcart

    return HttpResponseRedirect('/catalog/rentalcart/')