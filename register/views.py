from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.template import loader
from .user_registration import UserForm
from django.http import HttpResponse
from studentportal.models import *
# Create your views here.

def index(request):
	template = loader.get_template('register/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def home(request):
	if not request.user.is_authenticated:
		return render(request, 'register/user_registration_form.html')
	else:
		user=request.user
		template = loader.get_template('register/home.html')
		context = {'username':user.username}
		return HttpResponse(template.render(context,request))

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'register/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'register/home.html', {'username': username})
            else:
                return render(request , 'register/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'register/login.html', {'error_message': 'Invalid login'})
    return render(request, 'register/login.html')

class UserFormView(View):
	form_class = UserForm
	template_name = 'register/user_registration_form.html'
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST) 
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)

			if user is not None: 
				if user.is_active:
					login(request, user)
					return redirect('register:home')

		return render(request, self.template_name, {'form': form})
