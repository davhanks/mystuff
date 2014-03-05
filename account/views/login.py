from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from . import templater


def process_request(request):
	'''Show all objects in the db'''

	form = LoginForm(initial = {

        'username': '',
        'password': '',

        })

	form = LoginForm(request)
	if request.method == 'POST':
		form = LoginForm(request, request.POST)
		if form.is_valid():
			user = authenticate(username= form.cleaned_data['username'], password=form.cleaned_data['password'])
			login(request, user)





		return HttpResponse('<script>window.location.href="/account/"; </script>')

	template_vars = {
		'form' : form,

	}

	return templater.render_to_response(request, 'login.html', template_vars)


class LoginForm(forms.Form):
	username = forms.CharField(label="Username", required=True)
	password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput())

	# def clean(self):
	# 	if len(self.errors) ==0:

