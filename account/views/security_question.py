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
    
    user = mmod.User.objects.get(id=request.urlparams[0])

    now = timezone.now()

    valid_date = now + datetime.timedelta(hours=12)

    email_list = []

    error_code = 0
    error_mes = ''

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(now)
    print(valid_date)

    # for u in user_list:
    #     email_list.append(u.email)

    form = ResetPasswordForm(initial = {

        'security_answer': '',

        })

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            security_answer = form.cleaned_data['security_answer']
            key = randint(10000,1000000)

            if security_answer == user.security_answer:
                email = user.email
                pr = mmod.PasswordReset()
                pr.valid_date = valid_date
                pr.used = False
                pr.user_id = user.id
                pr.key = key
                pr.save()

                send_mail('DigitalMyWorld Password Reset', 'Go to localhost:8000/account/code_reset/ and enter your key: ' + str(key), 'davidkhanks@gmail.com',
                [email], fail_silently=False)
            # else:
            #     send_mail('DigitalMyWorld Password Reset', 'Your email was not found in our database. Are you sure you typed in the correct email?', 'davidkhanks@gmail.com',
            #     [email], fail_silently=False)


            return HttpResponseRedirect('/homepage/')


    template_vars = {
        'form': form,
        'error_code': error_code,
        'error_mes': error_mes,
    }

    return templater.render_to_response(request, 'forgot_password.html', template_vars)


class ResetPasswordForm(forms.Form):

    security_answer = forms.CharField()