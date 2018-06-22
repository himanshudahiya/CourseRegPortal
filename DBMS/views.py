from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from studentportal.models import *
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse
# Create your views here.
def index(request):
	return HttpResponse('<h2>Welcome User. Please Login!!</h2><a href="/studentportal/" target="_blank">Student Portal</a><br><a href="/facultyportal/" target="_blank">Faculty Portal</a><br><a href=" /dean_staff_office/" target="_blank">Dean Staff Portal</a>')