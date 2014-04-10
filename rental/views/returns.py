from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Get products from the DB'''
    users = mmod.User.objects.filter(is_active=True)

    user = request.user

    if not user.is_staff:
        return HttpResponseRedirect('/rental/user_return/user.id/')




    template_vars = {
        'users': users,
    }

    return templater.render_to_response(request, 'returns.html', template_vars)



def process_request__search(request):
    try:
        users = mmod.User.objects.filter(first_name__icontains=request.POST.get('first', '')).filter(last_name__icontains=request.POST.get('last', '')).filter(phone__icontains=request.POST.get('phone', ''))
    except User.DoesNotExist:
        users = mmod.User.ojects.none()

    if len(users)==0:
        try:
            users = mmod.User.objects.filter(first_name__icontains=request.POST.get('first', '')).filter(last_name__icontains=request.POST.get('last', ''))
        except User.DoesNotExist:
            users = mmod.User.objects.none()

    if len(users)==0:
        try:
            users = mmod.User.objects.filter(phone__icontains=request.POST.get('phone', ''))
        except User.DoesNotExist:
            users = mmod.User.objects.none()

    if len(users)==0:
        try:
            users = mmod.User.objects.filter(last_name__icontains=request.POST.get('last', ''))
        except User.DoesNotExist:
            users = mmod.User.objects.none()

    if len(users)==0:
        try:
            users = mmod.User.objects.filter(first_name__icontains=request.POST.get('first', ''))
        except User.DoesNotExist:
            users = mmod.User.objects.none()

    template_vars = {
        'users': users,
    }

    return templater.render_to_response(request, 'returns.html', template_vars)

# class LookupForm(forms.Form):
#     '''The Lookup form'''
#     first = forms.CharField()
#     last = forms.CharField()
#     phone = forms.CharField()
