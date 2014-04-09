from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Display the Edit Store form'''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/manager/dashboard')

    u = mmod.User.objects.get(id=request.urlparams[0])

    # run the form
    form = UserForm(initial={

        'username': u.username,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'email': u.email,
        'street': u.street,
        'street2': u.street2,
        'city': u.city,
        'state': u.state,
        'zipCode': u.zipCode,
        'phone': u.phone,
        'question': u.security_question,
        'answer': u.security_answer,
        'is_staff': u.is_staff,
    })
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u.username = form.cleaned_data['username']
            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            u.email = form.cleaned_data['email']
            u.street = form.cleaned_data['street']
            u.street2 = form.cleaned_data['street2']
            u.city = form.cleaned_data['city']
            u.state = form.cleaned_data['state']
            u.zipCode = form.cleaned_data['zipCode']
            u.phone = form.cleaned_data['phone']
            u.security_question = form.cleaned_data['question']
            u.security_answer = form.cleaned_data['answer']
            u.is_staff = form.cleaned_data['is_staff']
            u.save()
            return HttpResponseRedirect('/manager/userlist/')

    template_vars = {
        'form': form,
        'id': u.id,

    }

    return templater.render_to_response(request, 'edituser.html', template_vars)

class UserForm(forms.Form):
    '''The store edit form'''
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    street = forms.CharField()
    street2 = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    phone = forms.CharField()
    question = forms.CharField()
    answer = forms.CharField()
    is_staff = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(1, 'Yes'),(0, 'No')]))
