from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse

# Create your views here.
global error_message
error_message = ''
now = datetime.datetime.now()
def index(request):
	template = loader.get_template('studentportal/login.html')
	context = {}
	if request.session.has_key('student_id'):
		return home(request)
	return HttpResponse(template.render(context, request))

def login_user(request):
	if request.session.has_key('student_id'):
		return home(request)
	if request.method == "POST":
	    student_id = request.POST['username']
	    password = request.POST['password']
	    if student_id is not None:
	    	if student.objects.filter(student_id = student_id).exists():
	    		student_obj = student.objects.get(student_id = student_id)
		    	if student_obj is None:
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
	    	else:
		    	context = {'error_message': 'Invalid login'}
		    	template = loader.get_template('studentportal/login.html')
		    	return HttpResponse(template.render(context, request))
	return redirect('/studentportal/')


def logout_user(request):
	if request.session.has_key('student_id'):
		del request.session['student_id']
	return redirect('/studentportal/')
	
def home(request):
	if request.session.has_key('student_id'):
		student_id=request.session['student_id']
		template = loader.get_template('studentportal/home.html')
		student_obj = student.objects.get(student_id = student_id)
		takes_obj = takes.objects.filter(student_obj = student_obj)
		your_courses = []
		current_obj = current.objects.all()
		for obj in current_obj:
			current_year=obj.current_year
			current_sem=obj.current_sem
		for takes_t in takes_obj:
			if takes_t.teaches.year==current_year and takes_t.teaches.semester==current_sem:
				your_courses.append(takes_t.teaches)

					
				
		portal_objs = portalsOpen.objects.all()
		crp_open = False
		for portal_obj in portal_objs:
			crp_open = portal_obj.crp_open
		
		context = {'student_obj':student_obj,'your_courses':your_courses, 'crp_open':crp_open}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/studentportal/')
def view_grades(request):
	if request.session.has_key('student_id'):
		student_id=request.session['student_id']
		student_obj = student.objects.get(student_id = student_id)
		template = loader.get_template('studentportal/view_grades.html')
		grades_obj= grades.objects.filter(student_id = student_obj)
		print(grades_obj)
		context = {'student_obj':student_obj,'grades_obj':grades_obj}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/studentportal/')



		
def register_courses(request):
	if request.session.has_key('student_id'):

		portal_objs = portalsOpen.objects.all()
		crp_open = False
		for portal_obj in portal_objs:
			crp_open = portal_obj.crp_open
		if crp_open:
			student_id=request.session['student_id']
			template = loader.get_template('studentportal/register_courses.html')
			student_obj = student.objects.get(student_id = student_id)
			current_obj = current.objects.all()
			for obj in current_obj:
				current_year=obj.current_year
				current_sem=obj.current_sem


			to_your_batch = []
			to_other_batch = []
			teaches_objs_old = teaches.objects.filter(year = current_year, semester = student_obj.current_sem)
			teaches_objs = []
			print(teaches_objs_old)
			# takes_obj = takes.objects.filter(student_obj = student_obj)
			# your_courses = []
			# for takes_t in takes_obj:
			# 	for batch in takes_t.teaches.batch.all():
			# 		if student_obj.current_year == batch.year:
			# 			your_courses.append(takes_t.teaches)
			
			for teaches_obj_old in teaches_objs_old:
				teaches_objs.append(teaches_obj_old)

			# for your_courses_tt in your_courses:
			# 	if your_courses_tt not in teaches_objs:
			# 		teaches_objs.append(your_courses_tt)
			# 	elif your_courses_tt in teaches_objs:
			# 		teaches_objs.remove(your_courses_tt)
			
			for teaches_t in teaches_objs:
				for batch_t in teaches_t.batch.all():
					if batch_t.dept == student_obj.dept_id and batch_t.year == student_obj.current_year:
						if teaches_t in to_other_batch:
							to_other_batch.remove(teaches_t)
						if teaches_t not in to_your_batch:
							to_your_batch.append(teaches_t)
					elif teaches_t not in to_your_batch and teaches_t not in to_other_batch:
							to_other_batch.append(teaches_t)
			successful_registered = []
			tokened = []
			success_reg_obj = successfull_register.objects.filter(student_id = student_obj)
			for success_reg_objs in success_reg_obj:
				if success_reg_objs.teaches in to_your_batch:
					to_your_batch.remove(success_reg_objs.teaches)
				if success_reg_objs.teaches in to_other_batch:
					to_other_batch.remove(success_reg_objs.teaches)
				successful_registered.append(success_reg_objs.teaches)


			tokened_obj = token.objects.filter(student_obj = student_obj)
			for tokened_objs in tokened_obj:
				if tokened_objs.teaches in to_your_batch:
					to_your_batch.remove(tokened_objs.teaches)
				elif tokened_objs.teaches in to_other_batch:
					to_other_batch.remove(tokened_objs.teaches)
				tokened.append(tokened_objs.teaches)
			global error_message
			context = {'student_obj':student_obj, 
				'to_your_batch': to_your_batch,
				'to_other_batch': to_other_batch, 
			 	'successful_registered': successful_registered,
			 	'tokened': tokened,
			 	'error_message': error_message
			}
			error_message = ''
			return HttpResponse(template.render(context,request))
		else:
			return redirect('/studentportal/')

	else:
		return redirect('/studentportal/')



def add_course_batch(request):
	global error_message

	if request.session.has_key('student_id'):
		selected_course = request.POST['Add_Course']
		student_id=request.session['student_id']
		course_attr = selected_course.split('+')
		faculty_id = (course_attr[0])
		course_id = (course_attr[1])
		semester = int(course_attr[2])
		year = int(course_attr[3])
		slot = str(course_attr[4])


		student_obj = student.objects.get(student_id = student_id)
		faculty_id_obj = faculty.objects.get(faculty_id = faculty_id)
		course_id_obj = course.objects.get(course_id = course_id)
		course_tokened = False
		selected_course_obj = teaches.objects.get(faculty_id = faculty_id_obj, course_id = course_id_obj, semester = semester, year = year, slot = slot)
		# cgpa constraint
		takes_obj = takes.objects.filter(student_obj = student_obj)
		years = []
		for takes_t in takes_obj:
			for batch in takes_t.teaches.batch.all():
				years.append(batch.year)

		same_slot_courses = []
		successfull_register_objs = successfull_register.objects.filter(student_id = student_obj)
		for teaches_t in successfull_register_objs:
			if teaches_t.teaches.slot == slot:
				same_slot_courses.append(teaches_t)
		#same slot
		if len(same_slot_courses) > 0:
			global error_message
			error_message = 'You have a course registered in same slot.'
			return redirect('studentportal:register_courses')


		if selected_course_obj.min_cgpa_constraint > student_obj.cgpa:
			token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = 1, reason = "CGPA not satisfied")
			
			error_message = ''
			course_tokened = True
		
		course_credit = 0
		n = int(selected_course_obj.course_id.credit_struct)
		while n:
			course_credit, n = course_credit + n % 10, n // 10
		# credit limit
		if student_obj.curr_registered_credits + course_credit > student_obj.max_credit:
			if course_tokened == False:
				token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = 1, reason = "Credit limit not satisfied")
			else:
				token_tttt.reason = token_tttt.reason + " :and: " + "Credit limit not satisfied"
			
			error_message = ''
			token_tttt.save()
			course_tokened = True
		
		# prerequistes
		prerequistes_list = selected_course_obj.prerequisite.all()
		for prerequisite_tt in prerequistes_list:
			if teaches.objects.filter(course_id = prerequisite_tt.course_id).exists():
				prereq_teaches = teaches.objects.filter(course_id = prerequisite_tt.course_id)
				prereq_cleared = False
				for prereq_teaches_tt in prereq_teaches:
					if grades.objects.filter(student_id = student_obj, teaches = prereq_teaches_tt).exists():
						grades_obj_prereq = grades.objects.get(student_id = student_obj, teaches = prereq_teaches_tt)
						grade_prereq = grades_obj_prereq.grade
						if grade_prereq != 0:
							prereq_cleared = True
						else:
							if course_tokened == False:
								token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = 1, reason = "Prerequisite not cleared")
								course_tokened = True
							else:
								token_tttt.reason = token_tttt.reason + " :and: " + "Prerequisite not cleared"
								course_tokened = True
			else:
				if course_tokened == False:
					token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = 1, reason = "Prerequisite not cleared")
					course_tokened = True
				else:
					token_tttt.reason = token_tttt.reason + " :and: " + "Prerequisite not cleared"
					course_tokened = True


		if course_tokened:
			token_tttt.save()
			return redirect('studentportal:register_courses')


		if student_obj.curr_registered_credits + course_credit <= student_obj.max_credit:
			registered_courses_ttt = successfull_register(student_id = student_obj, teaches = selected_course_obj)
			registered_courses_ttt.save()
			student_obj.curr_registered_credits = student_obj.curr_registered_credits + course_credit
			student_obj.save()
			
			error_message = ''
			return redirect('studentportal:register_courses')

		return redirect('studentportal:register_courses')
	else:
		return redirect('/studentportal/')

def add_course_other_batch(request):
	global error_message
	if request.session.has_key('student_id'):
		selected_course = request.POST['Add_Course']
		student_id=request.session['student_id']
		course_attr = selected_course.split('+')
		faculty_id = (course_attr[0])
		course_id = (course_attr[1])
		semester = int(course_attr[2])
		year = int(course_attr[3])
		slot = str(course_attr[4])
		student_obj = student.objects.get(student_id = student_id)
		faculty_id_obj = faculty.objects.get(faculty_id = faculty_id)
		course_id_obj = course.objects.get(course_id = course_id)
		selected_course_obj = teaches.objects.get(faculty_id = faculty_id_obj, course_id = course_id_obj, semester = semester, year = year, slot = slot)
		# cgpa constraint
		takes_obj = takes.objects.filter(student_obj = student_obj)
		years = []
		for takes_t in takes_obj:
			for batch in takes_t.teaches.batch.all():
				years.append(batch.year)


		same_slot_courses = []
		successfull_register_objs = successfull_register.objects.filter(student_id = student_obj)
		for teaches_t in successfull_register_objs:
			if teaches_t.teaches.slot == slot:
				same_slot_courses.append(teaches_t)
		#same slot
		if len(same_slot_courses) > 0:
			global error_message
			error_message = 'You have a course registered in same slot.'
			print(error_message)
			return redirect('studentportal:register_courses')
		token_tttt = token(student_obj = student_obj,teaches = selected_course_obj,status = 1, reason = "Student is of other batch")
		if selected_course_obj.min_cgpa_constraint > student_obj.cgpa:
			token_tttt.reason = "CGPA not satisfied" + " :and: " + token_tttt.reason 
			
			error_message = ''
		
		course_credit = 0
		n = int(selected_course_obj.course_id.credit_struct)
		while n:
			course_credit, n = course_credit + n % 10, n // 10
		# credit limit
		if student_obj.curr_registered_credits + course_credit > student_obj.max_credit:
			# token_tttt.reason = token(student_obj = student_obj,teaches = selected_course_obj,status = 1, reason = "Credit limit not satisfied")
			token_tttt.reason = "Credit limit not satisfied" +  " :and: " + token_tttt.reason 
			
			error_message = ''


		prerequistes_list = selected_course_obj.prerequisite.all()
		for prerequisite_tt in prerequistes_list:
			if teaches.objects.filter(course_id = prerequisite_tt.course_id).exists():
				prereq_teaches = teaches.objects.filter(course_id = prerequisite_tt.course_id)
				prereq_cleared = False
				for prereq_teaches_tt in prereq_teaches:
					if grades.objects.filter(student_id = student_obj, teaches = prereq_teaches_tt).exists():
						grades_obj_prereq = grades.objects.get(student_id = student_obj, teaches = prereq_teaches_tt)
						grade_prereq = grades_obj_prereq.grade
						if grade_prereq != 0:
							prereq_cleared = True
						else:
							token_tttt.reason = token_tttt.reason + " :and: " + "Prerequisite not cleared"
			else:
				token_tttt.reason = token_tttt.reason + " :and: " + "Prerequisite not cleared"
				
		if student_obj.curr_registered_credits + course_credit <= student_obj.max_credit:
			
			error_message = ''
			token_tttt.save()
			return redirect('studentportal:register_courses')
		

		token_tttt.save()
		return redirect('studentportal:register_courses')
	else:
		return redirect('/studentportal/')

def delete_reg_course(request):
	global error_message
	if request.session.has_key('student_id'):
		selected_course = request.POST['Remove_Course']
		student_id=request.session['student_id']
		course_attr = selected_course.split('+')
		faculty_id = (course_attr[0])
		course_id = (course_attr[1])
		semester = int(course_attr[2])
		year = int(course_attr[3])
		slot = str(course_attr[4])
		student_obj = student.objects.get(student_id = student_id)
		faculty_id_obj = faculty.objects.get(faculty_id = faculty_id)
		course_id_obj = course.objects.get(course_id = course_id)
		selected_course_obj = teaches.objects.get(faculty_id = faculty_id_obj, course_id = course_id_obj, semester = semester, year = year, slot = slot)
		registered_courses_ttt = successfull_register.objects.get(student_id = student_obj, teaches = selected_course_obj).delete()
		course_credit = 0
		n = int(selected_course_obj.course_id.credit_struct)
		while n:
			course_credit, n = course_credit + n % 10, n // 10
		student_obj.curr_registered_credits = student_obj.curr_registered_credits - course_credit
		student_obj.save()
		return redirect('studentportal:register_courses')
	else:
		return redirect('/studentportal/')

def delete_tokened_course(request):
	if request.session.has_key('student_id'):
		selected_course = request.POST['Remove_Course']
		student_id=request.session['student_id']
		course_attr = selected_course.split('+')
		faculty_id = (course_attr[0])
		course_id = (course_attr[1])
		semester = int(course_attr[2])
		year = int(course_attr[3])
		slot = str(course_attr[4])
		student_obj = student.objects.get(student_id = student_id)
		faculty_id_obj = faculty.objects.get(faculty_id = faculty_id)
		course_id_obj = course.objects.get(course_id = course_id)
		selected_course_obj = teaches.objects.get(faculty_id = faculty_id_obj, course_id = course_id_obj, semester = semester, year = year, slot = slot)
		registered_courses_ttt = token.objects.get(student_obj = student_obj, teaches = selected_course_obj).delete()
		return redirect('studentportal:register_courses')
	else:
		return redirect('/studentportal/')


		