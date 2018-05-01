from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse
from .models import *
import datetime
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




# def register_courses(request, error_message=None):
# 	if request.session.has_key('student_id'):
# 		student_id=request.session['student_id']
# 		template = loader.get_template('studentportal/register_courses.html')
# 		student_obj = student.objects.get(student_id = student_id)
# 		current_year = now.year
# 		if student_obj.current_sem == 2:
# 			current_year = current_year - 1

# 		to_your_batch = []
# 		to_other_batch = []
# 		teaches_objs = teaches.objects.filter(year = current_year, semester = student_obj.current_sem)
# 		for teaches_t in teaches_objs:
# 			for batch_t in teaches_t.batch.all():
# 				if batch_t.dept == student_obj.dept_id and batch_t.year == student_obj.current_year:
# 					if teaches_t in to_other_batch:
# 						to_other_batch.remove(teaches_t)
# 					if teaches_t not in to_your_batch:
# 						to_your_batch.append(teaches_t)
# 				elif teaches_t not in to_your_batch and teaches_t not in to_other_batch:
# 						to_other_batch.append(teaches_t)
# 		successful_registered = []
# 		tokened = []
# 		success_reg_obj = successfull_register.objects.filter(student_id = student_obj)
# 		for success_reg_objs in success_reg_obj:
# 			if success_reg_objs.teaches in to_your_batch:
# 				to_your_batch.remove(success_reg_objs.teaches)
# 			successful_registered.append(success_reg_objs.teaches)

# 		tokened_obj = token.objects.filter(student_obj = student_obj)
# 		for tokened_objs in tokened_obj:
# 			if tokened_objs.teaches in to_your_batch:
# 				to_your_batch.remove(tokened_objs.teaches)
# 			elif tokened_objs.teaches in to_other_batch:
# 				to_other_batch.remove(tokened_objs.teaches)
# 			tokened.append(tokened_objs.teaches)

# 		context = {'student_obj':student_obj, 
# 			'to_your_batch': to_your_batch,
# 			'to_other_batch': to_other_batch, 
# 		 	'successful_registered': successful_registered,
# 		 	'tokened': tokened,
# 		 	'error_message': error_message
# 		}
# 		return HttpResponse(template.render(context,request))
# 	else:
# 		return redirect('/studentportal/')



# def add_course_batch(request):
# 	selected_course = request.POST['Add_Course']
# 	student_id=request.session['student_id']
# 	course_attr = selected_course.split('+')
# 	faculty_id = (course_attr[0])
# 	course_id = (course_attr[1])
# 	section_id = str(course_attr[2])
# 	semester = int(course_attr[3])
# 	year = int(course_attr[4])
# 	slot = str(course_attr[5])

# 	# takes_obj = takes.objects.filter(student_obj = student_obj)
# 	# current_courses = []
# 	# years = []
# 	# for takes_t in takes_obj:
# 	# 	for batch in takes_t.teaches.batch.all():
# 	# 		years.append(batch.year)

# 	# for takes in takes_obj:
# 	# 	if student_obj.current_sem == takes.teaches.semester:
# 	# 		for year in years:
# 	# 			if year == student_obj.current_year:
# 	# 				current_courses.append(takes)
# 	student_obj = student.objects.get(student_id = student_id)
# 	faculty_id_obj = faculty.objects.get(faculty_id = faculty_id)
# 	course_id_obj = course.objects.get(course_id = course_id)
# 	selected_course_obj = teaches.objects.get(faculty_id = faculty_id_obj, course_id = course_id_obj, section_id = section_id, semester = semester, year = year, slot = slot)
# 	error_message = ''
# 	print(selected_course_obj)
# 	# cgpa constraint
# 	if selected_course_obj.min_cgpa_constraint > student_obj.cgpa:
# 		token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = "CGPA not satisfied")
# 		token_tttt.save()
# 		return register_courses(request, error_message)
# 	takes_obj = takes.objects.filter(student_obj = student_obj)
# 	years = []
# 	for takes_t in takes_obj:
# 		for batch in takes_t.teaches.batch.all():
# 			years.append(batch.year)

# 	taken_this_year = []
# 	for takes_t in takes_obj:
# 		if student_obj.current_sem == takes_t.teaches.semester:
# 			for year in years:
# 				if year == student_obj.current_year:
# 					taken_this_year.append(takes_t)

# 	same_slot_courses = []
# 	for teaches_t in taken_this_year:
# 		if teaches_t.teaches.slot == slot:
# 			same_slot_courses.append(teaches_t)
# 	#same slot
# 	if len(same_slot_courses) > 0:
# 		error_message = 'You have a course registered in same slot.'
# 		return register_courses(request, error_message)
# 	course_credit = 0
# 	n = int(selected_course_obj.course_id.credit_struct)
# 	while n:
# 		course_credit, n = course_credit + n % 10, n // 10
# 	# credit limit
# 	if student_obj.curr_registered_credits + course_credit > student_obj.max_credit:
# 		token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = "Credit limit not satisfied")
# 		token_tttt.save()
# 		return register_courses(request, error_message)
	



	
