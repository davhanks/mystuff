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
        
    products = mmod.Product.objects.all()
    stores = mmod.Store.objects.all()

    template_vars = {
        'products': products,
        'stores': stores,

    }

    return templater.render_to_response(request, 'rent.html', template_vars)






#     def process_request__add(request):

#     # get cart
#     rentalcart = request.session.get('rentalcart', {})
#     product = mmod.Product.objects.get(id__in=request.urlparams[0])

#     print(str(product.id) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
#     # # if item exists in cart, add 1 else put item in cart with quantity of 1
#     if str(product.id) in rentalcart:
#         print("<<<<<<<<<<<<<<<<<<Already in cart")
#         return HttpResponseRedirect('/catalog/rentals/' + request.urlparams[1] + '/')
#     else:
#         rentalcart[str(product.id)] = product.store_id
#         request.session['rentalcart'] = rentalcart
#     for key in rentalcart:
#         print("key: " + key + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         print("Value: " + str(rentalcart[key]) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


#     return HttpResponseRedirect('/catalog/rent/')

# def process_request__remove(request):

#     rentalcart = request.session.get('rentalcart', {})
#     del rentalcart[request.urlparams[0]]
#     request.session['rentalcart'] = rentalcart

#     return HttpResponseRedirect('/catalog/rentalcart/')