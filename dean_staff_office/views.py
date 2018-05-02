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
	template = loader.get_template('dean_staff_office/login.html')
	context = {}
	if request.session.has_key('staff_id'):
		return home(request)
	return HttpResponse(template.render(context, request))
global error_message
error_message=''
global good_message
good_message = ''

def add_hod(request):
	template =loader.get_template('dean_staff_office/add.html')
	context = {}
	faculty_obj=faculty.objects.all()
	departments=department.objects.all()
	context = {'faculty_obj':faculty_obj,'departments':departments}
	print(faculty_obj)
	if request.session.has_key('staff_id'):
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def hod_db(request):
	global error_message
	error_message=''
	
	if request.session.has_key('staff_id'):
		

		faculty_id=request.POST['faculty']
		faculty_obj=faculty.objects.get(faculty_id=faculty_id)
		print(faculty_obj)
		dept=faculty_obj.dept_id
		hod_obj=hod.objects.filter(dateto=None)
		if hod_obj.exists:
			for hods in hod_obj:
				if hods.faculty_obj.dept_id  is dept:
					hods.faculty_obj.dateto=datetime.datetime.now()

		




		
		
		hod_obj = hod(faculty_id=faculty_obj,datefrom=datetime.datetime.now())
		hod_obj.save()
		return redirect('/dean_staff_office/add_hod')


		



		
	else:
		return redirect('/dean_staff_office/')


def add_advisor(request):
	template =loader.get_template('dean_staff_office/add_advisor.html')
	context = {}
	faculty_obj=faculty.objects.all()
	batch_obj=batch.objects.all()
	context = {'faculty_obj':faculty_obj,'batch_obj':batch_obj}
	print(faculty_obj)
	if request.session.has_key('staff_id'):
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def advisor_db(request):
	
	if request.session.has_key('staff_id'):
		

		faculty_id=request.POST['faculty']
		batch_str=request.POST['batch']
		
		batch_attr=batch_str.split('+')
		year=int(batch_attr[0])
		print(year)
		dept_id=int(batch_attr[1])
		dept_obj=department.objects.get(dept_id=dept_id)
		batch_add=batch.objects.get(year=year,dept=dept_obj)

		faculty_obj=faculty.objects.get(faculty_id=faculty_id)
		
		advisor_obj = advisor(faculty_id=faculty_obj,batch=batch_add)
		advisor_obj.save()
		return redirect('/dean_staff_office/add_advisor')
	else:
		return redirect('/dean_staff_office/')






# def add_advisor(request):
# 	template =loader.get_template('dean_staff_office/add.html')
# 	context = {}
# 	faculty_obj=faculty.objects.all()
# 	departments=department.objects.all()
# 	context = {'faculty_obj':faculty_obj,'departments':departments}
# 	if request.session.has_key('staff_id'):
# 		return HttpResponse(template.render(context,request))
# 	else:
# 		return redirect('/dean_staff_office/')
# # def add_advisor(request):
# 	template loader.get_template('dean_staff_office/add.html')
# 	context = {}
# 	if request.session.has_key('staff_id'):
# 		return HttpResponse(template.render(context,request))
# 	else:
# 		return redirect('/dean_staff_office/')







def login_user(request):
	if request.session.has_key('staff_id'):
		return home(request)
	if request.method == "POST":
	    staff_id = request.POST['username']
	    password = request.POST['password']
	    if staff_id is not None:
	    	if dean_staff_office.objects.filter(staff_id = staff_id).exists():
		    	staff_obj = dean_staff_office.objects.get(staff_id = staff_id)
		    	if staff_obj is None:
		        	context = {
		        		'error_message': 'Invalid login'
		        	}
		        	template = loader.get_template('dean_staff_office/login.html')
		        	return HttpResponse(template.render(context, request))
		    	elif staff_obj is not None:
		        	if staff_obj.password == password:
		        		request.session['staff_id'] = staff_id
		        		return redirect('/dean_staff_office/home')
		        	else:
		        		context = {'error_message': 'Invalid login'}
		        		template = loader.get_template('dean_staff_office/login.html')
		        		return HttpResponse(template.render(context, request))
		    	else:
		        	context = {
		        		'error_message': 'Invalid login'
		        	}
		        	template = loader.get_template('dean_staff_office/login.html')
		        	return HttpResponse(template.render(context, request))
	    	else:
		   		context = {'error_message': 'Invalid login'}
		   		template = loader.get_template('dean_staff_office/login.html')
		   		return HttpResponse(template.render(context, request))
	return redirect('/dean_staff_office/')


def logout_user(request):
	if request.session.has_key('staff_id'):
		del request.session['staff_id']
	return redirect('/dean_staff_office/')
	
def home(request):
	if request.session.has_key('staff_id'):
		staff_id=request.session['staff_id']
		template = loader.get_template('dean_staff_office/home.html')
		staff_obj = dean_staff_office.objects.get(staff_id = staff_id)
		context = {'staff_obj':staff_obj}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def course_catalogue(request):
	if request.session.has_key('staff_id'):
		staff_id=request.session['staff_id']
		template = loader.get_template('dean_staff_office/course_catalogue.html')
		staff_obj = dean_staff_office.objects.get(staff_id = staff_id)
		course_catalogue_objs = course.objects.all()
		dept_objs = department.objects.all()
		header_count = len(dept_objs)
		depts_courses = [[] for i in range(0, header_count)]
		print(header_count)
		print(depts_courses)
		for course_catalogue_obj in course_catalogue_objs:
			depts_courses[int(course_catalogue_obj.dept_id.dept_id)-1].append(course_catalogue_obj)
		print(depts_courses)
		context = {'staff_obj':staff_obj, 'depts_courses': depts_courses, 'dept_objs': dept_objs}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def add_course(request):
	if request.session.has_key('staff_id'):
		staff_id=request.session['staff_id']
		template = loader.get_template('dean_staff_office/add_course.html')
		dept_objs = department.objects.all()
		global error_message
		global good_message
		context = {'dept_objs':dept_objs,'error_message':error_message, 'good_message':good_message}
		error_message = ''
		good_message = ''
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')

def course_post(request):
	print("add course post")
	if request.session.has_key('staff_id'):
		print('session valid')
		if request.method == "POST":
			print("method is post")
			course_id = request.POST['course_id']
			course_title = request.POST['course_title']
			course_ltp = request.POST['course_ltp_struct']
			course_dept = request.POST['course_dept']
			dept_obj = department.objects.get(dept_id = course_dept)

			if course.objects.filter(course_id = course_id).exists():
				global error_message
				error_message = "Course already exist!!"
			else:
				global good_message
				good_message = "Course added! Add another course."
				course_obj = course(course_id = course_id, credit_struct = course_ltp, title = course_title, dept_id= dept_obj)
				course_obj.save()
			return redirect('/dean_staff_office/add_course')
		else:
			return redirect('/dean_staff_office/')
	else:
		return redirect('/dean_staff_office/')


def edit_course(request, course_id):
	if request.session.has_key('staff_id'):
		course_obj = course.objects.get(course_id = str(course_id))
		dept_objs = department.objects.all()
		context = {'dept_objs':dept_objs, 'course_obj':course_obj}
		template = loader.get_template('dean_staff_office/add_course.html')
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')


def course_edit_post(request, course_id_prev):
	if request.session.has_key('staff_id'):
		course_id = request.POST['course_id']
		course_title = request.POST['course_title']
		course_ltp = request.POST['course_ltp_struct']
		course_dept = request.POST['course_dept']
		dept_obj = department.objects.get(dept_id = course_dept)
		if course_id_prev == course_id:
			course_obj = course.objects.get(course_id = course_id_prev)
			course_obj.course_id = course_id
			course_obj.title = course_title
			course_obj.credit_struct = course_ltp
			course_obj.dept_id = dept_obj
			course_obj.save()
		elif course.objects.filter(course_id = course_id).exists():
			global error_message
			error_message = "Course with id = " + course_id + " already exists"
			return redirect('/dean_staff_office/edit_course/' + course_id_prev) 
		else:
			course_obj = course.objects.get(course_id = course_id_prev).delete()
			course_obj_new = course(course_id = course_id, title = course_title, credit_struct = course_ltp, dept_id = dept_obj)
			course_obj_new.save()

		return redirect('/dean_staff_office/course_catalogue/')

	else:
		return redirect('/dean_staff_office/')




def student_catalogue(request):
	if request.session.has_key('staff_id'):
		student_objs = student.objects.all()
		template = loader.get_template('dean_staff_office/student_catalogue.html')
		dept_objs = department.objects.all()
		context = {'student_objs': student_objs, 'dept_objs': dept_objs}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')


def add_student(request):
	if request.session.has_key('staff_id'):
		template = loader.get_template('dean_staff_office/add_student.html')
		dept_objs = department.objects.all()
		global error_message
		global good_message
		context = {'dept_objs':dept_objs,'error_message':error_message, 'good_message':good_message}
		error_message = ''
		good_message = ''
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')


def student_post(request):
	if request.session.has_key('staff_id'):
		if request.method == "POST":
			student_id = request.POST['student_id']
			student_name = request.POST['student_title']
			student_dept = request.POST['student_dept']
			dept_obj = department.objects.get(dept_id = student_dept)

			if student.objects.filter(student_id = student_id).exists():
				global error_message
				error_message = "Student already exist!!"
			else:
				global good_message
				good_message = "Student added! Add another student."
				student_email = student_id+"@iitrpr.ac.in"
				student_obj = student(student_id = student_id, name = student_name, dept_id = dept_obj, student_email = student_email)
				student_obj.save()
			return redirect('/dean_staff_office/add_student')
		else:
			return redirect('/dean_staff_office/')
	else:
		return redirect('/dean_staff_office/')


def edit_student(request, student_id):
	if request.session.has_key('staff_id'):
		student_obj = student.objects.get(student_id = student_id)
		dept_objs = department.objects.all()
		global error_message
		context = {'dept_objs':dept_objs, 'student_obj':student_obj, 'error_message': error_message}
		error_message = ''
		template = loader.get_template('dean_staff_office/add_student.html')
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')


def student_edit_post(request, student_id_prev):
	if request.session.has_key('staff_id'):
		student_id = request.POST['student_id']
		student_name = request.POST['student_title']
		student_dept = request.POST['student_dept']
		dept_obj = department.objects.get(dept_id = student_dept)
		if student_id_prev == student_id:
			student_obj = student.objects.get(student_id = student_id_prev)
			student_obj.name = student_name
			student_obj.dept_id = dept_obj
			student_obj.save()
		elif student.objects.filter(student_id = student_id).exists():
			global error_message
			error_message = "Student with id = " + student_id + " already exists"
			return redirect('/dean_staff_office/edit_student/' + student_id_prev)
		else:
			student_obj = student.objects.get(student_id = student_id_prev).delete()
			student_email = student_id + "@iitrpr.ac.in"
			student_obj_new = student(student_id=student_id, name=student_name, dept_id = dept_obj, student_email = student_email)
			student_obj_new.save()
		return redirect('/dean_staff_office/student_catalogue/')
	else:
		return redirect('/dean_staff_office/')




def faculty_catalogue(request):
	if request.session.has_key('staff_id'):
		faculty_objs = faculty.objects.all()
		template = loader.get_template('dean_staff_office/faculty_catalogue.html')
		dept_objs = department.objects.all()
		context = {'faculty_objs': faculty_objs, 'dept_objs': dept_objs}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')


def add_faculty(request):
	if request.session.has_key('staff_id'):
		template = loader.get_template('dean_staff_office/add_faculty.html')
		dept_objs = department.objects.all()
		global error_message
		global good_message
		context = {'dept_objs':dept_objs,'error_message':error_message, 'good_message':good_message}
		error_message = ''
		good_message = ''
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')


def faculty_post(request):
	if request.session.has_key('staff_id'):
		if request.method == "POST":
			faculty_id = request.POST['faculty_id']
			faculty_name = request.POST['faculty_title']
			faculty_dept = request.POST['faculty_dept']
			dept_obj = department.objects.get(dept_id = faculty_dept)

			if faculty.objects.filter(faculty_id = faculty_id).exists():
				global error_message
				error_message = "Faculty already exist!!"
			else:
				global good_message
				good_message = "Faculty added! Add another faculty."
				faculty_email = faculty_id+"@iitrpr.ac.in"
				faculty_obj = faculty(faculty_id = faculty_id, name = faculty_name, dept_id = dept_obj, email_id = faculty_email)
				faculty_obj.save()
			return redirect('/dean_staff_office/add_faculty')
		else:
			return redirect('/dean_staff_office/')
	else:
		return redirect('/dean_staff_office/')


def edit_faculty(request, faculty_id):
	if request.session.has_key('staff_id'):
		faculty_obj = faculty.objects.get(faculty_id = faculty_id)
		dept_objs = department.objects.all()
		global error_message
		context = {'dept_objs':dept_objs, 'faculty_obj':faculty_obj, 'error_message': error_message}
		error_message = ''
		template = loader.get_template('dean_staff_office/add_faculty.html')
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')


def faculty_edit_post(request, faculty_id_prev):
	if request.session.has_key('staff_id'):
		faculty_id = request.POST['faculty_id']
		faculty_name = request.POST['faculty_title']
		faculty_dept = request.POST['faculty_dept']
		dept_obj = department.objects.get(dept_id = faculty_dept)
		if faculty_id_prev == faculty_id:
			faculty_obj = faculty.objects.get(faculty_id = faculty_id_prev)
			faculty_obj.name = faculty_name
			faculty_obj.dept_id = dept_obj
			faculty_obj.save()
		elif faculty.objects.filter(faculty_id = faculty_id).exists():
			global error_message
			error_message = "faculty with id = " + faculty_id + " already exists"
			return redirect('/dean_staff_office/edit_faculty/' + faculty_id_prev)
		else:
			faculty_obj = faculty.objects.get(faculty_id = faculty_id_prev).delete()
			faculty_email = faculty_id + "@iitrpr.ac.in"
			faculty_obj_new = faculty(faculty_id=faculty_id, name=faculty_name, dept_id = dept_obj, email_id = faculty_email)
			faculty_obj_new.save()
		return redirect('/dean_staff_office/faculty_catalogue/')
	else:
		return redirect('/dean_staff_office/')
