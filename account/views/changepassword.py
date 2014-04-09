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

    u = request.user
    error_code = 0
    error_mes = ''

    form = ChangePasswordForm(initial = {

        'password': '',
        'retype': '',


        })

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            password = form.cleaned_data['password']
            retype = form.cleaned_data['retype']


            if password != retype:
                error_code = 1


            if error_code == 1:
                error_mes = 'Passwords must match'
                
            
            if error_code == 0:
                u.set_password(password)
                u.save()
                return HttpResponseRedirect('/account/accountDashboard/')


            


    template_vars = {
        'form': form,
        'error': error_mes,

    }

    return templater.render_to_response(request, 'changepassword.html', template_vars)

def process_request__reset(request):

    code = request.session.get('code','')

    if code == '':
        return HttpResponseRedirect('/homepage/')

    pr = mmod.PasswordReset.objects.get(id=code)
    u = mmod.User.objects.get(id=pr.user_id)
    error_code = 0
    error_mes = ''


    form = ChangePasswordForm(initial = {

        'password': '',
        'retype': '',


        })

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            password = form.cleaned_data['password']
            retype = form.cleaned_data['retype']


            if password != retype:
                error_code = 1
                error_mes = 'Passwords must match'
                
            
            if error_code == 0:
                u.set_password(password)
                u.save()
                pr.used = True
                pr.save()
                request.session['code'] = ''
                return HttpResponseRedirect('/homepage/')


            


    template_vars = {
        'form': form,
        'error': error_mes,

    }

    return templater.render_to_response(request, 'changepassword.html', template_vars)


class ChangePasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())
    retype = forms.CharField(widget=forms.PasswordInput())
