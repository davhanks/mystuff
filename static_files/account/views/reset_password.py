from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from django.core.mail import send_mail
import datetime
from django.utils import timezone


def process_request(request):
    
    user_list = mmod.User.objects.all()

    now = timezone.now()

    valid_date = now + datetime.timedelta(days=1)

    email_list = []

    for u in user_list:
        email_list.append(u.email)

    form = ResetPasswordForm(initial = {

        'email': '',
        'security_answer': '',

        })

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            security_answer = form.cleaned_data['security_answer']

            if email in email_list:
                user = mmod.User.objects.get(email=email)
                pr = mmod.PasswordReset()
                pr.valid_date = valid_date
                pr.used = False
                pr.user_id = user.id
                pr.save()

                send_mail('DigitalMyWorld Password Reset', 'Follow this link to reset your password.', 'davidkhanks@gmail.com',
                [email], fail_silently=False)
            else:
                send_mail('DigitalMyWorld Password Reset', 'Your email was not found in our database. Are you sure you typed in the correct email?', 'davidkhanks@gmail.com',
                [email], fail_silently=False)


            return HttpResponseRedirect('/homepage/')


    template_vars = {
        'form': form,

    }

    return templater.render_to_response(request, 'forgot_password.html', template_vars)


class ResetPasswordForm(forms.Form):

    email = forms.EmailField()
    security_answer = forms.CharField()