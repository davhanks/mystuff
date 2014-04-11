from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import *
from django.utils import timezone



def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[0])
    rentals = mmod.Rental.objects.filter(user_id=user.id).exclude(returned=True)
    now = datetime.now()


    print('>>>>>>>>>>>>>>>>>')
    print(now)

    return_items = []    


    template_vars = {
        'user': user,
        'rentals':rentals,
        'now': now,
    }

    return templater.render_to_response(request, 'user_return.html', template_vars)



