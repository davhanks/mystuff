from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from random import randint
from datetime import datetime
from django.core.mail import send_mail
import requests


def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[0])

    # begin_date = request.session['begin']
    # end_date = request.session['end']

    repaircart = request.session.get('repaircart', {})
    catalog = mmod.CatalogInventory.objects.all()
    repairs = []
    remove = []
    user = mmod.User.objects.get(id=request.urlparams[0])
    now = datetime.now()
    total_repair_fee = 0

    error_code = 0

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

            for key in repaircart:
                if repaircart[key] == user.id:
                    sr = mmod.ServiceRepair.objects.get(id=key)
                    repairs.append(sr)
                    remove.append(key)

            for r in remove:
                if repaircart[r] == user.id:
                    del repaircart[r]

            request.session['repaircart'] = repaircart

            card_number = form.cleaned_data['card_number']
            cvn = form.cleaned_data['cvn']
            exp_date = form.cleaned_data['exp_date']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipCode = form.cleaned_data['zipCode']
            
            for ServiceRepair in repairs:
                total_repair_fee += ServiceRepair.labor_hours

            charge_amount = total_repair_fee * 10.5
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
              'cvc': int(cvn),
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
                error_code = 1

            if error_code == 0:
                for ServiceRepair in repairs:
                    ServiceRepair.bill_street = street
                    ServiceRepair.bill_city = city
                    ServiceRepair.bill_state = state
                    ServiceRepair.bill_zipCode = zipCode

                    ServiceRepair.creditCardNum = card_number
                    ServiceRepair.cvn = cvn
                    ServiceRepair.card_first = first_name
                    ServiceRepair.card_last = last_name
                    ServiceRepair.expDate = exp_date

                    ServiceRepair.receipt_number = randint(10000,1000000)

                    ServiceRepair.picked_up = True
                    ServiceRepair.pickup_date = now

                    ServiceRepair.amount = ServiceRepair.labor_hours * 10.5
                    ServiceRepair.save()

                send_mail('DigitalMyWorld Repair', 'Your repair has been picked up!', 'davidkhanks@gmail.com',
                [user.email], fail_silently=False)

                
                return HttpResponseRedirect('/repair/userlookup/')


    template_vars = {
        'user': user,
        'form': form,
        'repairs': repairs,
        'catalog': catalog,
        'error_code': error_code,
    }

    return templater.render_to_response(request, 'repair_checkout.html', template_vars)

class CardForm(forms.Form):
    '''The billing address form'''
    card_number = forms.CharField()
    cvn = forms.CharField()
    exp_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    first_name = forms.CharField()
    last_name = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    