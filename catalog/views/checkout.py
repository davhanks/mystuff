from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
from random import randint


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    if request.user.is_staff:
        commission = True


    # run the form
    uid = request.user.id
    u = mmod.User.objects.get(id=uid)
    cart = request.session.get('cart', {})
    products = []


    # Flat rate shipping and a var for storing the subtotal
    subtotal = 0
    shipping_charge = 10.00
    com_amount = 0


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


        # Create the sale object and all related B.O.s and confirm the order
        sale = mmod.Sale()
        sale.user_id = u.id
        
            # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        sale.date = datetime.now()
        sale.sub_total = subtotal
        sale.shipping_cost = 0
        # total = subtotal + shipping_charge


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

        sale.receipt_number = 1234
        sale.save()

        

        # makes a saleitem for every conceptual item in the cart
        for prod in products:
            # gets the quantity of the current item
            quantity = cart[str(prod.id)]
            prod_com = prod.commission_rate * prod.sale_price * quantity
            com_amount += prod_com

            # gets the list of all physical items that have not been sold that match the current
            # conceptual inv item and creates a sale item
            pp = mmod.Product.objects.filter(catalog_inventory_id = prod.id).filter(active=True)
            for i in range(0,quantity):
                saleItem = mmod.SaleItem()
                saleItem.sale_id = sale.id
                saleItem.product_id = pp[i].id
                saleItem.save()


        if commission:
            com = mmod.Commission()
            com.employee_id = u.id
            com.sale_id = sale.id
            com.date = datetime.now()
            com.amount = com_amount
            com.save()



        return HttpResponseRedirect('/catalog/receipt/')

            
    template_vars = {
        'form1' : form1,
        'form2' : form2,
        'form3' : form3,

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
