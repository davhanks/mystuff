from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/manager/login/')
    user = request.user
            


    template_vars = {
        'user' : user,
    }

    return templater.render_to_response(request, 'accountDashboard.html', template_vars)
