from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from .models import *
# Create your views here.


def index(request):
	template = loader.get_template('studentportal/login.html')
	context = {}
	return HttpResponse(template.render(context, request))

def login_user(request):
	if request.method == "POST":
	    student_id = request.POST['username']
	    password = request.POST['password']
	    if student_id is not None:
	    	student_obj = student.objects.get(student_id = student_id)
	        if student is None:
	        	context = {
	        		'error_message': 'Invalid login'
	        	}
	        	template = loader.get_template('studentportal/login.html')
	        	return HttpResponse(template.render(context, request))
	        elif student_obj is not None:
	        	if student_obj.password == password:
	        		request.session['student_id'] = student_id
	        		return redirect('/studentportal/home')
	        	else:
	        		context = {'error_message': 'Invalid login'}
	        		template = loader.get_template('studentportal/login.html')
	        		return HttpResponse(template.render(context, request))
	        else:
	        	context = {
	        		'error_message': 'Invalid login'
	        	}
	        	template = loader.get_template('studentportal/login.html')
	        	return HttpResponse(template.render(context, request))
	template = loader.get_template('studentportal/login.html')
	return HttpResponse(template.render({}, request))


def logout_user(request):
	del request.session['student_id']
	template = loader.get_template('studentportal/login.html')
	return HttpResponse(template.render({}, request))
	
def home(request):
	if request.session.has_key('student_id'):
		student_id=request.session['student_id']
		template = loader.get_template('studentportal/home.html')
		student_obj = student.objects.get(student_id = student_id)
		context = {'username':student_obj.name}
		return HttpResponse(template.render(context,request))
	else:
		template = loader.get_template('studentportal/login.html')
		context = {}
		return redirect('/studentportal/')
		return HttpResponse(template.render(context,request))
		



