from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')

    form = UserForm(initial={

        'first_name': u.first_name,
        'last_name': u.last_name,
        'email': u.email,
        'street': u.street,
        'street2': u.street2,
        'city': u.city,
        'state': u.state,
        'zipCode': u.zipCode,
        'phone': u.phone,
    })

    if request.method == 'POST':
        

        form = NewUserForm(request.POST)
        if form.is_valid():

            u = mmod.User.objects.create_user(request.POST['username'], form.cleaned_data['email'], request.POST['password'])

            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            u.street = form.cleaned_data['street']
            u.city = form.cleaned_data['city']
            u.state = form.cleaned_data['state']
            u.zipCode = form.cleaned_data['zipCode']
            u.phone = form.cleaned_data['phone']
            
            

            for u in users:
                if u.username == username:
                    error_code = 1
                if password != retype:
                    error_code = 2
                else:
                    
            


    template_vars = {
        'form': form,
        'error': error_code,

    }

    return templater.render_to_response(request, 'userinfo.html', template_vars)


class UserInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    street = forms.CharField()
    street2 = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    phone = forms.CharField()




    # if request.method == 'POST':
    #     form = NewUserForm(request.POST)
    #     if form.is_valid():
    #         password = form.cleaned_data['password']
    #         retype = form.cleaned_data['retype']
    #         credentials = {
    #             'username': form.cleaned_data['username'],
    #             'password': form.cleaned_data['password']
    #         }
    #         for u in users:
    #             if u.username == username:
    #                 error_code = 1
    #             if password != retype:
    #                 error_code = 2
    #             else:
    #                 return templater.render_to_response(request, 'userinfo.html', credentials)