from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout


def process_request(request):
	'''Logout'''
	logout(request)

	return HttpResponseRedirect('/homepage/')