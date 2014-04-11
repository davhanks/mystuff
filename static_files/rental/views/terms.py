from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from random import randint
from datetime import datetime, timedelta
import requests
from django.core.mail import send_mail


def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[0])
    request.session['current_user'] = 'None'
    request.session['current_user'] = user.id
    request.session['rental'] = 'None'
    rentalcart = request.session.get('rentalcart', {})
    catalog = mmod.CatalogInventory.objects.all()
    products = []
    error_code = 0
    charge_amount = 0

    for key in rentalcart:
        prod = mmod.Product.objects.get(id=key)
        products.append(prod)
        charge_amount += prod.rental_fee

    form = TermsForm()
    form2 = CardForm()


    if request.method == 'POST':
        form = TermsForm(request.POST)
        form2 = CardForm(request.POST)
        if form.is_valid():
            begin_date = form.cleaned_data['begin_date']
            end_date = form.cleaned_data['end_date']

            days = end_date - begin_date
            print('>>>>>>>>>>>>>>>>>>>>>>>' + str(begin_date))
            print('>>>>>>>>>>>>>>>>>>>>>>>' + str(end_date))
            print(days.days)

            num_days = days.days

            charge_amount *= num_days


        if form2.is_valid():

            first_name = form2.cleaned_data['first_name']
            last_name = form2.cleaned_data['last_name']
            street = form2.cleaned_data['street']
            city = form2.cleaned_data['city']
            state = form2.cleaned_data['state']
            zipCode = form2.cleaned_data['zipCode']
            card_number = form2.cleaned_data['card_number']
            cvn = form2.cleaned_data['cvn']
            exp_date = form2.cleaned_data['exp_date']


        rest_charge = str(charge_amount)

        full_name = first_name + ' ' + last_name
        
        # Test Number: 4732817300654
        # Test CVN: 411

        # send the request with the data
        API_URL = 'http://dithers.cs.byu.edu/iscore/api/v1/charges'
        API_KEY = 'b6a57a6b718b756064393dd12588130d'
        r = requests.post(API_URL, data={
          'apiKey': API_KEY,
          'currency': 'usd',
          'amount': rest_charge,
          'type': 'Visa',
          'number': card_number,
          'exp_month': 10,
          'exp_year': 14,
          'cvc': 411,
          'name': full_name,
          'description': 'Charge for: ' + full_name,
        })

        # just for debugging, print the response text
        print(r.text)

        # parse the response to a dictionary
        resp = r.json()
        # print(resp['ID'])
        if 'error' in resp:
            # raise forms.ValidationError(resp['error'])
            error_code = 2  

        if end_date < begin_date:
            error_code = 1

        if error_code == 0:
            dateDue = end_date + timedelta(hours=17)

            r = mmod.Rental()
            r.dateOut = begin_date
            r.dateDue = dateDue
            # r.dateIn = None
            # r.work_order = randint(10000,1000000)
            r.user_id = user.id

            r.street = street
            r.city = city
            r.state = state
            r.zipCode = zipCode

            r.creditCardNum = card_number
            r.cvn = cvn
            r.card_first = first_name
            r.card_last = last_name
            r.expDate = exp_date

            r.receipt_number = randint(10000,1000000)
            r.save()
            request.session['rental'] = r.id

            for p in products:
                ri = mmod.RentalItem()
                ri.rental_id = r.id
                ri.product_id = p.id
                ri.save()

                p.rented_out = True
                p.times_rented += 1
                p.save()

                send_mail('DigitalMyWorld Rental', 'Thank you for choosing DigitalMyWorld! Your rental is now active.', 'davidkhanks@gmail.com',
                [user.email], fail_silently=False)
            return HttpResponseRedirect('/rental/userlookup/')


    template_vars = {
        'user': user,
        'form': form,
        'form2': form2,
        'products': products,
        'catalog': catalog,
        'error_code': error_code,
    }

    return templater.render_to_response(request, 'terms.html', template_vars)



  
class TermsForm(forms.Form):
    '''The Lookup form'''
    begin_date = forms.DateField(label='', widget=forms.TextInput(attrs={'class': 'datepicker formHeight', 'placeholder':'Begin Date'}))
    end_date = forms.DateField(label='', widget=forms.TextInput(attrs={'class': 'datepicker formPad', 'placeholder':'End Date'}))
    
class CardForm(forms.Form):
    '''The billing address form'''
    first_name = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-size'}))
    last_name = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-size'}))
    street = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Street', 'class':'form-size'}))
    street2 = forms.CharField(required=False, label = '', widget=forms.TextInput(attrs={'placeholder':'Apt or Suite', 'class':'form-size'}))
    city = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'City', 'class':'form-size'}))
    state = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'State', 'class':'form-size'}))
    zipCode = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Zip Code', 'class':'form-size'}))
    card_number = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Card Number', 'class':'form-size'}))
    cvn = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'CVN', 'class':'form-size'}))
    exp_date = forms.DateField(label='', widget=forms.TextInput(attrs={'placeholder':'Exp Date','class':'datepicker form-size'}))