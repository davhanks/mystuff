from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from django.contrib.auth import authenticate, login
from . import templater


def process_request(request):
    '''Display the Login form'''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/manager/dashboard/')



    # run the form
    form = LoginForm(initial={

        'username': '',
        'password': '',

    })
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print(">>>>>>>>>>>>>>>>>>>>>>User is valid, active and authenticated")
                    login(request, user)
                    if user.is_staff:
                        return HttpResponseRedirect('/manager/dashboard/')
                    else:
                        return HttpResponseRedirect('/homepage/index/')
                else:
                    print(">>>>>>>>>>>>>>>>>>>>>>The password is valid, but the account has been disabled!")
                    return HttpResponseRedirect('/manager/login/')
            else:
                # the authentication system was unable to verify the username and password
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>The username and password were incorrect.")
                return HttpResponseRedirect('/manager/login/')



    template_vars = {
        'form': form

    }

    return templater.render_to_response(request, 'login.html', template_vars)

class LoginForm(forms.Form):
    '''The login form'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password= self.cleaned_data.get('password'))
        if user == None:
            raise forms.ValidationError('Invalid username or password')

        return self.cleaned_data