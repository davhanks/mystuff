from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
from random import randint
from django.core.mail import send_mail
import requests


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    commission = False
    if request.user.is_staff:
        commission = True

    error_code = 0


    # run the form
    uid = request.user.id
    u = mmod.User.objects.get(id=uid)
    cart = request.session.get('cart', {})
    products = []
    soldList = []


    # Flat rate shipping and a var for storing the subtotal
    subtotal = 0
    shipping_charge = 10.00

    # Amount of commissions for this sale (this is always calculated but not saved if 
    # it is an online sale)
    com_amount = 0

    COGS = 0


    # gets the products from the cart
    for key in cart:
        prod = mmod.CatalogInventory.objects.get(id__in=key)
        products.append(prod)

        subtotal += (prod.sale_price * cart[key])

    form1 = ShipForm(initial={

        'Ship_first' : 'stupid face',
        'Ship_last' : '',
        'street': '',
        'city': '',
        'state': '',
        'zipCode': '',

    })

    form2 = BillForm(initial={

    'street': '',
    'city': '',
    'state': '',
    'zipCode': '',

    })

    form3 = CardForm(initial={

    'card_number': '',
    'cvn' : '',
    'first_name': '',
    'last_name': '',
    'exp_date': '',

    })
    if request.method == 'POST':
        ship_first = ''
        ship_last = ''
        ship_street = ''
        ship_city = ''
        ship_state = ''
        ship_zipCode = ''

        bill_street = ''
        bill_city = ''
        bill_state = ''
        bill_zipCode = ''

        card_cc_num = ''
        card_cvn = ''
        card_first = ''
        card_last = ''
        card_exp_date = ''


        form1 = ShipForm(request.POST)
        if form1.is_valid():

            ship_first = form1.cleaned_data['ship_first']
            ship_last = form1.cleaned_data['ship_last']
            ship_street = form1.cleaned_data['street']
            ship_city = form1.cleaned_data['city']
            ship_state = form1.cleaned_data['state']
            ship_zipCode = form1.cleaned_data['zipCode']

        form2 = BillForm(request.POST)
        if form2.is_valid():

            bill_street = form2.cleaned_data['street']
            bill_city = form2.cleaned_data['city']
            bill_state = form2.cleaned_data['state']
            bill_zipCode = form2.cleaned_data['zipCode']

        form3 = CardForm(request.POST)
        if form3.is_valid():
            card_cc_num = form3.cleaned_data['card_number']
            card_cvn = form3.cleaned_data['cvn']
            card_first = form3.cleaned_data['first_name']
            card_last = form3.cleaned_data['last_name']
            card_exp_date = form3.cleaned_data['exp_date']

        

        # send the request with the data
        API_URL = 'http://dithers.cs.byu.edu/iscore/api/v1/charges'
        API_KEY = 'b6a57a6b718b756064393dd12588130d'
        r = requests.post(API_URL, data={
          'apiKey': API_KEY,
          'currency': 'usd',
          'amount': '5.99',
          'type': 'Visa',
          'number': card_cc_num,
          'exp_month': 10,
          'exp_year': 14,
          'cvc': 411,
          'name': 'Cosmo Limesandal',
          'description': 'Charge for cosmo@is411.byu.edu',
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
            # Create the sale object and all related B.O.s and confirm the order
            sale = mmod.Sale()
            sale.user_id = u.id
            
                # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            sale.date = datetime.now()
            sale.sub_total = subtotal
            sale.shipping_cost = 10.00
            # total = float(subtotal) + shipping_charge


            sale.tax_ammount = 0

            sale.ship_first = ship_first
            sale.ship_last = ship_last
            sale.ship_street = ship_street
            sale.ship_city = ship_city
            sale.ship_state = ship_state
            sale.ship_zipCode = ship_zipCode

            sale.bill_street = bill_street
            sale.bill_city = bill_city
            sale.bill_state = bill_state
            sale.bill_zipCode = bill_zipCode

            sale.creditCardNum = card_cc_num
            sale.cvn = card_cvn
            sale.card_first = card_first
            sale.card_last = card_last
            sale.expDate = card_exp_date

            sale.receipt_number = randint(10000,1000000)
            sale.save()

            

            # makes a saleitem for every conceptual item in the cart
            for prod in products:
                # gets the quantity of the current item
                quantity = cart[str(prod.id)]

                # calculates the commission for each conceptual product times quantity
                prod_com = prod.commission_rate * prod.sale_price * quantity

                # adds that amount to the total commissions for this sal
                com_amount += prod_com

                # calulates the COGS sold for this item times quantity
                prod_cogs = prod.average_cost * quantity

                # adds that amount to the total COGS for this sale
                COGS += prod_cogs

                # gets the list of all physical items that have not been sold that match the current
                # conceptual inv item and creates a sale item
                pp = mmod.Product.objects.filter(catalog_inventory_id = prod.id).filter(active=True)
                for i in range(0,quantity):
                    saleItem = mmod.SaleItem()
                    saleItem.sale_id = sale.id
                    saleItem.product_id = pp[i].id
                    saleItem.save()

                    # add each id to a list to set them as sold after a Sale Item object is created
                    soldList.append(pp[i].id)

            cart = {}
            request.session['cart'] = cart

            # Set each sold Physical Product to false so that it can only be sold once
            for p in soldList:
                prod = mmod.Product.objects.get(id=p)
                prod.active = False
                prod.save()

            # if an employee is performing the sale, calculate commission and save it
            if commission:
                com = mmod.Commission()
                com.employee_id = u.id
                com.sale_id = sale.id
                com.date = datetime.now()
                com.amount = com_amount
                com.save()

            request.session['sale_id'] = sale.id
            # request.session['total'] = total

            send_mail('DigitalMyWorld Purchase!', 'Thank you for your purchase!', 'davidkhanks@gmail.com',
                    [u.email], fail_silently=False)
            

            return HttpResponseRedirect('/catalog/receipt/')

            
    template_vars = {
        'form1' : form1,
        'form2' : form2,
        'form3' : form3,
        'error_code': error_code,

    }

    return templater.render_to_response(request, 'checkout.html', template_vars)

class ShipForm(forms.Form):
    '''The Shipping address form'''
    ship_first = forms.CharField()
    ship_last = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()

class BillForm(forms.Form):
    '''The billing address form'''
    street = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()

class CardForm(forms.Form):
    '''The billing address form'''
    card_number = forms.CharField()
    cvn = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    exp_date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))
