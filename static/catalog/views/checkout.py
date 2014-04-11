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
    sales_tax = 0.00

    # get the list of general ledger name objects
    gln = mmod.GeneralLedgerName.objects.all()

    # if the user is a staff member the sale is taking place in the store therefore
    # commissions and sales tax need to be accounted for. Otherwise these two values are set
    # to False and 0.00% respectively
    if request.user.is_staff:
        commission = True
        sales_tax = 0.0795

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

    # initialize this variable for later use for the accounting entries for each sale
    COGS = 0


    # gets the products from the cart
    for key in cart:
        prod = mmod.CatalogInventory.objects.get(id__in=key)
        products.append(prod)

        subtotal += (prod.sale_price * cart[key])
        COGS += (prod.average_cost * cart[key])

    form1 = ShipForm(initial = {
            'ship_first': u.first_name,
            'ship_last': u.last_name,
            'ship_street': u.street,
            'ship_street2': u.street2,
            'ship_city': u.city,
            'ship_state': u.state,
            'ship_zipCode': u.zipCode,

        })

    form2 = BillForm()

    form3 = CardForm()


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
            ship_street = form1.cleaned_data['ship_street']
            ship_city = form1.cleaned_data['ship_city']
            ship_state = form1.cleaned_data['ship_state']
            ship_zipCode = form1.cleaned_data['ship_zipCode']

        form2 = BillForm(request.POST)
        if form2.is_valid():

            bill_first = form2.cleaned_data['bill_first']
            bill_last = form2.cleaned_data['bill_last']
            bill_street = form2.cleaned_data['bill_street']
            bill_city = form2.cleaned_data['bill_city']
            bill_state = form2.cleaned_data['bill_state']
            bill_zipCode = form2.cleaned_data['bill_zipCode']

        form3 = CardForm(request.POST)
        if form3.is_valid():
            card_cc_num = form3.cleaned_data['card_number']
            card_cvn = form3.cleaned_data['cvn']
            card_first = form3.cleaned_data['first_name']
            card_last = form3.cleaned_data['last_name']
            card_exp_date = form3.cleaned_data['exp_date']

        charge_amount = sales_tax + float(shipping_charge) + float(subtotal)
        rest_charge = str(charge_amount)

        full_name = bill_first + ' ' + bill_last
        
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
          'number': card_cc_num,
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
            error_code = 1


        if error_code == 0:
            # Create the sale object and all related B.O.s and confirm the order
            sale = mmod.Sale()
            sale.user_id = u.id
            
                # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            sale.date = datetime.now()

            # Line item amounts of the sale
            sale.sub_total = subtotal
            sale.shipping_cost = shipping_charge
            sale.tax_ammount = float(subtotal) * sales_tax
            sale.amount = charge_amount

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

            # Accounting entries follow*************************

            # Journal entry for sale
            jourEntry = mmod.JournalEntry()
            jourEntry.revenueSource_id = sale.id
            jourEntry.date = datetime.now()
            jourEntry.save()

            # Receipt of cash
            debitCash = mmod.Debit()
            debitCash.GeneralLedgerName_id = gln[0].id
            debitCash.journalEntry_id = jourEntry.id
            debitCash.amount = sale.sub_total
            debitCash.save()

            # Credit Sales
            creditSales = mmod.Credit()
            creditSales.GeneralLedgerName_id = gln[1].id
            creditSales.journalEntry_id = jourEntry.id
            creditSales.amount = sale.sub_total
            creditSales.save()

            # COGS
            debitCOGS = mmod.Debit()
            debitCOGS.GeneralLedgerName_id = gln[2].id
            debitCOGS.journalEntry_id = jourEntry.id
            debitCOGS.amount = COGS
            debitCOGS.save()

            # Credit Inventory
            creditInventory = mmod.Credit()
            creditInventory.GeneralLedgerName_id = gln[3].id
            creditInventory.journalEntry_id = jourEntry.id
            creditInventory.amount = COGS
            creditInventory.save()




            

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
    ship_first = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-size'}))
    ship_last = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-size'}))
    ship_street = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Street', 'class':'form-size'}))
    ship_street2 = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Apt or Suite', 'class':'form-size'}))
    ship_city = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'City', 'class':'form-size'}))
    ship_state = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'State', 'class':'form-size'}))
    ship_zipCode = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Zip Code', 'class':'form-size'}))

class BillForm(forms.Form):
    '''The billing address form'''
    bill_first = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-size'}))
    bill_last = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-size'}))
    bill_street = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Street', 'class':'form-size'}))
    bill_street2 = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Apt or Suite', 'class':'form-size'}))
    bill_city = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'City', 'class':'form-size'}))
    bill_state = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'State', 'class':'form-size'}))
    bill_zipCode = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Zip Code', 'class':'form-size'}))

class CardForm(forms.Form):
    '''The billing address form'''
    first_name = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-size'}))
    last_name = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-size'}))
    card_number = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Card Number', 'class':'form-size'}))
    cvn = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'CVN', 'class':'form-size'}))
    exp_date = forms.DateField(label = '', widget=forms.TextInput(attrs={'id':'datepicker', 'placeholder':'Exp Date', 'class':'form-size'}))
