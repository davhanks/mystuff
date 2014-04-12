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
    


    form = CheckEmailForm(initial = {

        'email': '',

        })

    if request.method == 'POST':
        form = CheckEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user_list = mmod.User.objects.all()


            for u in user_list:
                if u.email == email:
                    return HttpResponseRedirect('/account/security_question/' + str(u.id) + '/')




            


    template_vars = {
        'form': form,

    }

    return templater.render_to_response(request, 'forgot_password.html', template_vars)


class CheckEmailForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'width1'}))