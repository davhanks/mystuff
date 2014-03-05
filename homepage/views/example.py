from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from homepage import models as hmod
from . import templater


def process_request(request):
	'''Show all objects in the db'''
	questions = hmod.Question.objects.all()
	print(">>>>>>>>>>>>>>", questions)

	template_vars = {
		'questions': questions,
		'hey': 'there'

	}

	return templater.render_to_response(request, 'example.html', template_vars)