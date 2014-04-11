from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
	'''Show all objects in the db'''
	products = mmod.CatalogInventory.objects.all()



	template_vars = {
		'prods': products,


	}

	return templater.render_to_response(request, 'index.html', template_vars)