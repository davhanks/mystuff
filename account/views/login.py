from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from . import templater
from django.contrib.auth import authenticate, login


def process_request(request):
    '''Show all objects in the db'''

    form = LoginForm(initial = {

        'username': '',
        'password': '',

        })

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username= form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # the password verified for the user
                if user.active:
                    print(">>>>>>>>>>>>>>>>>>>>>>User is valid, active and authenticated")
                    login(request, user)
                    if user.is_staff:
                        return HttpResponse('<script>window.location.href="/manager/dashboard"; </script>')
                    else:
                        return HttpResponse('<script>window.location.href="/account/"; </script>')






        # return HttpResponse('<script>window.location.href="/account/"; </script>')

    template_vars = {
        'form' : form,

    }

    return templater.render_to_response(request, 'login.html', template_vars)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput())

    # def clean(self):
    #   if len(self.errors) ==0:

