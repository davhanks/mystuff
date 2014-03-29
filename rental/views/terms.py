from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[0])
    rentalcart = request.session.get('rentalcart', {})
    catalog = mmod.CatalogInventory.objects.all()
    products = []

    for key in rentalcart:
        prod = mmod.Product.objects.get(id=key)
        products.append(prod)

    form = TermsForm()

    # if request.method == 'POST':
    #     form = TermsForm(request.POST)
    #     if form.is_valid():



    template_vars = {
        'user': user,
        'form': form,
        'products': products,
        'catalog': catalog,
    }

    return templater.render_to_response(request, 'terms.html', template_vars)



  
class TermsForm(forms.Form):
    '''The Lookup form'''
    begin = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker formHeight', 'placeholder':'Begin Date'}))
    days = forms.CharField(widget=forms.TextInput(attrs={'class': 'datepicker formPad', 'placeholder':'# of Days'}))
    rate = forms.DecimalField(widget=forms.TextInput(attrs={'id': 'rate', 'class':'formPad',  'placeholder':'Rate Per Day'}), decimal_places=2)
    
