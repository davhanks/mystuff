from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from random import randint
from datetime import datetime
from django.core.mail import send_mail


def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.session['current_user'])
    number = request.session['rental']
    rental = mmod.Rental.objects.get(id=number)

    # begin_date = request.session['begin']
    # end_date = request.session['end']

    rentalcart = request.session.get('rentalcart', {})
    catalog = mmod.CatalogInventory.objects.all()
    products = []
    error_code = 0

    for key in rentalcart:
        prod = mmod.Product.objects.get(id=key)
        products.append(prod)

    form = CardForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'street': user.street,
        'city': user.city,
        'state': user.state,
        'zipCode': user.zipCode,
        
        })

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipCode = form.cleaned_data['zipCode']
            card_number = form.cleaned_data['card_number']
            cvn = form.cleaned_data['cvn']
            exp_date = form.cleaned_data['exp_date']

            # if end_date < begin_date:
            #     error_code = 1

          

            if error_code == 0:

                rental.bill_street = street
                rental.bill_city = city
                rental.bill_state = state
                rental.bill_zipCode = zipCode

                rental.creditCardNum = card_number
                rental.cvn = cvn
                rental.card_first = first_name
                rental.card_last = last_name
                rental.expDate = exp_date

                rental.receipt_number = randint(10000,1000000)
                rental.save()

                send_mail('DigitalMyWorld Rental', 'Thank you for choosing DigitalMyWorld! Your rental is now active.', 'davidkhanks@gmail.com',
                [user.email], fail_silently=False)

                return HttpResponseRedirect('/rental/rentalreceipt/')


    template_vars = {
        'user': user,
        'form': form,
        'products': products,
        'catalog': catalog,
        'error_code': error_code,
    }

    return templater.render_to_response(request, 'rental_checkout.html', template_vars)

class CardForm(forms.Form):
    '''The billing address form'''
    first_name = forms.CharField()
    last_name = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    card_number = forms.CharField()
    cvn = forms.CharField()
    exp_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))