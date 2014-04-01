from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from django.contrib.auth import authenticate, login


def process_request(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    

    users = mmod.User.objects.all()
    error_code = 0
    error_mes = ''

    form = NewAccountForm(initial = {
        'username': '',
        'password': '',
        'retype': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'street': '',
        'street2': '',
        'city': '',
        'state': '',
        'zipCode': '',
        'phone': '',
        'is_Staff': True,

        })

    if request.method == 'POST':
        form = NewAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype = form.cleaned_data['retype']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            street = form.cleaned_data['street']
            street2 = form.cleaned_data['street']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipCode = form.cleaned_data['zipCode']
            phone = form.cleaned_data['phone']


            if password != retype:
                error_code = 2
            for u in users:
                if u.username == username:
                    error_code = 1
                    break

            if error_code == 1:
                error_mes = 'This username is already in use'
            elif error_code == 2:
                error_mes = 'Passwords must match'
            
            if error_code == 0:
                u = mmod.User.objects.create_user(username, email, password)
                u.first_name = first_name
                u.last_name = last_name
                u.street = street
                u.street2 = street2
                u.city = city
                u.state = state
                u.zipCode = zipCode
                u.phone = phone
                u.active = True
                u.is_active = True
                u.is_Staff = False
                u.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    # the password verified for the user
                    if user.is_active:
                        print(">>>>>>>>>>>>>>>>>>>>>>User is valid, active and authenticated")
                        login(request, user)
                        return HttpResponseRedirect('/homepage/index/')



            


    template_vars = {
        'form': form,
        'error': error_mes,

    }

    return templater.render_to_response(request, 'createaccount.html', template_vars)


class NewAccountForm(forms.Form):


    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    retype = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    street = forms.CharField()
    street2 = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    phone = forms.CharField()
