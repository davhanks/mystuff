from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from . import templater
from django.contrib.auth import authenticate, login
from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC, GET_ALL_INFO

def process_request(request):
    '''Login form'''

    form = LoginForm(initial = {

        'username': '',
        'password': '',

        })

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] + '@digitalmyworld.local'
            password = form.cleaned_data['password']
            try:
                s = Server('128.187.61.42', port=636, get_info = GET_ALL_INFO)
                c = Connection(s, user = username, password = password, auto_bind = True)
                print(s.info)

                result = c.search('o=test', '(objectClass=*)', SEARCH_SCOPE_WHOLE_SUBTREE, attributes=['sn', 'objectClass'])
                
                c.unbind()
            except Exception as e:
                print(e)


            user = authenticate(username= form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print(">>>>>>>>>>>>>>>>>>>>>>User is valid, active and authenticated")
                    
                    if user.is_staff:
                        return HttpResponse('<script>window.location.href="/manager/dashboard/"; </script>')
                    else:
                        return HttpResponse('<script>window.location.href="/homepage/"; </script>')






        # return HttpResponse('<script>window.location.href="/account/"; </script>')

    template_vars = {
        'form' : form,
    }

    return templater.render_to_response(request, 'login.html', template_vars)


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user == None:
            raise forms.ValidationError('Incorrect username or password')
        return self.cleaned_data

