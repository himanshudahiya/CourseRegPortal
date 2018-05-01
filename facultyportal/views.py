from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from .models import *
import datetime
import datetime
now = datetime.datetime.now()
# Create your views here.
now = datetime.datetime.now()
def index(request):
	template = loader.get_template('facultyportal/login.html')
	context = {}
	if request.session.has_key('faculty_id'):
		return home(request)
	return HttpResponse(template.render(context, request))

def login_user(request):
	if request.session.has_key('faculty_id'):
		return home(request)
	if request.method == "POST":
	    faculty_id = request.POST['username']
	    password = request.POST['password']
	    if faculty_id is not None:
	    	faculty_obj = faculty.objects.get(faculty_id = faculty_id)
	    	if faculty_obj is None:
	        	context = {
	        		'error_message': 'Invalid login'
	        	}
	        	template = loader.get_template('facultyportal/login.html')
	        	return HttpResponse(template.render(context, request))
	    	elif faculty_obj is not None:
	        	if faculty_obj.password == password:
	        		request.session['faculty_id'] = faculty_id
	        		return redirect('/facultyportal/home')
	        	else:
	        		context = {'error_message': 'Invalid login'}
	        		template = loader.get_template('facultyportal/login.html')
	        		return HttpResponse(template.render(context, request))
	    	else:
	        	context = {
	        		'error_message': 'Invalid login'
	        	}
	        	template = loader.get_template('facultyportal/login.html')
	        	return HttpResponse(template.render(context, request))
	template = loader.get_template('facultyportal/login.html')
	return redirect('/facultyportal/')


def logout_user(request):
	if request.session.has_key('faculty_id'):
		del request.session['faculty_id']
	return redirect('/facultyportal/')
	
def home(request):
	if request.session.has_key('faculty_id'):
		faculty_id=request.session['faculty_id']
		template = loader.get_template('facultyportal/home.html')
		faculty_obj = faculty.objects.get(faculty_id = faculty_id)
		teaches_obj = teaches.objects.filter(faculty_id = faculty_id)
		current_obj = current.objects.all()
		for obj in current_obj:
			current_year=obj.current_year
			current_sem=obj.current_sem
		print(current_year)
		print(current_sem)
		print(teaches_obj)

	#		for batch in takes_t.teaches.batch.all():
	#			years.append(batch.year)
	#	context = {'faculty_obj':faculty_obj,'takes_obj':takes_obj, 'years': years}
		context = {'faculty_obj':faculty_obj,'teaches_obj':teaches_obj,'current_year':current_year,'current_sem':current_sem}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/facultyportal/')

def grade(request, course_id):
	if request.session.has_key('faculty_id'):
		faculty_id=request.session['faculty_id']
		template = loader.get_template('facultyportal/grade.html')
		# faculty_id=faculty.objects.filter(faculty_id=faculty_id)
		current_obj = current.objects.all()
		for obj in current_obj:
			current_year=obj.current_year
			current_sem=obj.current_sem
		teaches_obj=teaches.objects.filter(faculty_id=faculty_id,year=current_year,semester=current_sem,course_id=course_id)
		takes_obj = takes.objects.filter(teaches=teaches_obj[0])

		print(teaches_obj)
		print(takes_obj)
		
		
	#		for batch in takes_t.teaches.batch.all():
	#			years.append(batch.year)
	#	context = {'faculty_obj':faculty_obj,'takes_obj':takes_obj, 'years': years}
		context = {'faculty_id':faculty_id,'takes_obj':takes_obj,'current_year':current_year,'current_sem':current_sem}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/facultyportal/')
		
def update_grade(request,student_id,course_id):
	if request.session.has_key('faculty_id'):
		faculty_id=request.session['faculty_id']

		grade=request.POST['grade']
		print(student_id)
		print(course_id)
		# id_attr = two_id.split('+')
		# print(two_id,id_attr)

		# student_id = id_attr[0]
		# course_id = id_attr[1]
		student_obj=student.objects.filter(student_id=student_id)
		current_obj = current.objects.all()
		for obj in current_obj:
			current_year=obj.current_year
			current_sem=obj.current_sem
		teaches_obj=teaches.objects.filter(faculty_id=faculty_id,year=current_year,semester=current_sem,course_id=course_id)
		grade_obj=grades.objects.filter(student_id=student_obj,teaches=teaches_obj)
		if(grade_obj) is None:
			grade_obj = grades(student_id=student_obj,teaches=teaches_obj,grade=grade)
			grade_obj.save()

		else:
			grade_obj.grade=grade

		return redirect('/facultyportal/grade/'+course_id)
	else:
		return redirect('/facultyportal/')





def float_new_courses(request):
	if request.session.has_key('faculty_id'):
		faculty_id=request.session['faculty_id']
		template = loader.get_template('facultyportal/float_new_courses.html')

		current_obj = current.objects.all()
		for obj in current_obj:
			current_year = obj.current_year
			current_sem = obj.current_sem


		batch_list = []
		batch_obj = batch.objects.all()
		
		faculty_obj = faculty.objects.get(faculty_id = faculty_id)
		faculty_dept_id = faculty_obj.dept_id
		
		c_dept = course.objects.filter(dept_id = faculty_dept_id)
		courses_of_dept=[]

		for c in c_dept:
			if(not teaches.objects.filter(course_id = c.course_id , faculty_id = faculty_id).exists()):
				courses_of_dept.append(c)
	
		context = {'courses_of_dept':courses_of_dept, 
				   'batch_obj':batch_obj
			
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/facultyportal/')


def add_course_float(request):
	faculty_id = request.session['faculty_id']
	faculty_obj = faculty.objects.get(faculty_id = faculty_id)
	course_id = request.POST['course_floated']
	print(course_id)
	course_obj = course.objects.get(course_id = course_id)
	current_obj = current.objects.all()
	for obj in current_obj:
		current_year = obj.current_year
		current_sem = obj.current_sem 
	slot = request.POST['slot']
	min_cg = request.POST['min_cg']

	batch_tt = request.POST.getlist('batches')
	batch_obj_list = []
	for b in batch_tt:
		ba = b.split('+')
		print(ba)
		year = ba[1]
		dept = ba[0]
		print(dept)
		dept_obj = department.objects.get(dept_id = dept)
		bat = batch.objects.get(year = year , dept = dept_obj)
		batch_obj_list.append(bat)

	prereq_tt = request.POST.getlist('prerequisite')
	prereq_obj_list = []
	for b in prereq_tt:
		prereq_obj = course.objects.get(course_id = b)
		prereq_obj_list.append(prereq_obj)
		


	teach = teaches(faculty_id = faculty_obj,course_id = course_obj, year = current_year , semester = current_sem , slot = slot , min_cgpa_constraint =min_cg)
	teach.save()
	for batch_list in batch_obj_list:
		teach.batch.add(batch_list)
	teach.save()

	for prereq_list in prereq_obj_list:
		teach.prerequisite.add(prereq_list)
	teach.save()		
	return redirect('/facultyportal/home/')
