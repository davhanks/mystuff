from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from django.core.mail import send_mail
import datetime
from django.utils import timezone
from random import randint


def process_request(request):
    

    error_code = 0
    error_mes = ''


    form = CodeResetForm(initial = {

        'reset_code': '',

        })

    if request.method == 'POST':
        form = CodeResetForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['reset_code']
            now = datetime.datetime.now()

            pr = mmod.PasswordReset.objects.filter(used=False, key=key).first()

            if pr == None:
                error_code = 1
                error_mes = 'This code is expired. Please resubmit your email for a new code.'
                # return HttpResponseRedirect('/homepage/')

            if error_code == 0:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print(now)
                print(pr.valid_date)
                if now < pr.valid_date:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    print('The key matched!')
                    request.session['code'] = pr.id
                    return HttpResponseRedirect('/account/changepassword__reset')
                    # pr.valid_date = valid_date
                    # pr.used = False
                    # pr.user_id = user.id
                    # pr.key = key
                    # pr.save()

                    # send_mail('DigitalMyWorld Password Reset', 'Go to localhost:8000/account/code_reset/ and enter your key: ' + str(key), 'davidkhanks@gmail.com',
                    # [email], fail_silently=False)
                # else:
                #     send_mail('DigitalMyWorld Password Reset', 'Your email was not found in our database. Are you sure you typed in the correct email?', 'davidkhanks@gmail.com',
                #     [email], fail_silently=False)


                # return HttpResponseRedirect('/homepage/')


    template_vars = {
        'form': form,
        'error_code': error_code,
        'error_mes': error_mes,

    }

    return templater.render_to_response(request, 'forgot_password.html', template_vars)


class CodeResetForm(forms.Form):

    reset_code = forms.CharField()