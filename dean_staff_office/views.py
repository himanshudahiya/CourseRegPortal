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
	global error_message
	
	global good_message
	
	context = {'faculty_obj':faculty_obj,'departments':departments,'error_message':error_message,'good_message':good_message}
	error_message=''
	good_message=''
	print(faculty_obj)
	if request.session.has_key('staff_id'):
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def hod_db(request):
	global error_message
	
	global good_message
	
	if request.session.has_key('staff_id'):
		faculty_id=request.POST['faculty']
		faculty_obj=faculty.objects.get(faculty_id=faculty_id)
		dept=faculty_obj.dept_id
		dept_form=request.POST['dept']
		dept_form_obj=department.objects.get(dept_id=dept_form)

		if dept != dept_form_obj:
			error_message='Not of same department'
			return redirect('/dean_staff_office/add_hod')
		

		else:
			hod_obj=hod.objects.all()
			if hod_obj is not None:
				for hods in hod_obj:
					if hods.faculty_id.dept_id  == dept:
						hods.delete()
			good_message='Added succesfully'
			hod_obj = hod(faculty_id=faculty_obj)
			hod_obj.save()
		return redirect('/dean_staff_office/add_hod')
					
					
		
	else:
		return redirect('/dean_staff_office/')


def add_advisor(request):
	template =loader.get_template('dean_staff_office/add_advisor.html')
	context = {}
	faculty_obj=faculty.objects.all()
	batch_obj=batch.objects.all()
	global error_message
	
	global good_message
	
	context = {'faculty_obj':faculty_obj,'batch_obj':batch_obj,'error_message':error_message,'good_message':good_message}
	error_message=''
	good_message=''
	print(faculty_obj)
	if request.session.has_key('staff_id'):
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def advisor_db(request):
	global error_message
	
	global good_message
	
	
	if request.session.has_key('staff_id'):
		

		faculty_id=request.POST['faculty']
		batch_str=request.POST['batch']
		
		batch_attr=batch_str.split('+')
		year=int(batch_attr[0])
		print(year)
		dept_id=int(batch_attr[1])
		faculty_obj=faculty.objects.get(faculty_id=faculty_id)
		dept_obj=department.objects.get(dept_id=dept_id)
		batch_add=batch.objects.get(year=year,dept=dept_obj)


		if(dept_obj !=faculty_obj.dept_id):
			error_message='Not of same department'
		else:
			advisor_obj=advisor.objects.filter(batch=batch_add)
			if advisor_obj is not None:
				advisor_obj.delete()
			good_message='Added succesfully'
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




def update_sem_year_form(request):
	if request.session.has_key('staff_id'):
		template = loader.get_template('dean_staff_office/update_sem_year_form.html')
		global error_message
		global good_message
		context ={'error_message':error_message, 'good_message':good_message}
		error_message=''
		good_message = ''
		return HttpResponse(template.render(context, request))
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


def update_sem_year(request):
	if request.session.has_key('staff_id'):
		updated_year = int(request.POST['year'])
		updated_sem = int(request.POST['sem'])

		current_objs = current.objects.all()
		curr_year=0
		for curr in current_objs:
			curr_year = curr.current_year
		student_objs = student.objects.all()
		print(curr_year)
		print(updated_year)	
		if((updated_year == curr_year+1) or (updated_year==curr_year)):
			for student_obj in student_objs:
				prev_cgpa = student_obj.cgpa
				prev_credit = student_obj.total_credits
				current_obj = current.objects.all()
				for obj in current_obj:
					curr_year=obj.current_year
					curr_sem=obj.current_sem
				if(curr_sem == 1):
					prev_sem = 2
					prev_year = curr_year -1
				elif(curr_sem == 2):
					prev_sem = 1
					prev_year = curr_year
				course_stu_list = grades.objects.filter(student_id = student_obj)
				sums = 0
				add_credit = 0
				prev_sem_credit=0
				for c in course_stu_list:
					if(int(c.grade)>=4 and c.teaches.semester == prev_sem and c.teaches.year == prev_year ):
						course_obj = course.objects.get(course_id = c.teaches.course_id.course_id)
						credit = course_obj.credit_struct
						t_credit = 0
						for d in credit:
							t_credit=t_credit+int(d)
						prev_sem_credit = prev_sem_credit+t_credit
					elif(int(c.grade)>=4 and c.teaches.semester == curr_sem and c.teaches.year == curr_year ):
						course_obj = course.objects.get(course_id = c.teaches.course_id.course_id)
						credit = course_obj.credit_struct
						t_credit = 0
						for d in credit:
							t_credit=t_credit+int(d)
						add_credit = add_credit + t_credit
						sums = sums + t_credit*int(c.grade)
				if student_obj.total_credits+add_credit != 0:
					sums = (sums + prev_cgpa*student_obj.total_credits)/(student_obj.total_credits+add_credit)
				student_obj.total_credits = student_obj.total_credits+add_credit
				student_obj.cgpa =  sums
				div=2
				if student_obj.current_year==1 and student_obj.current_sem==1:
					div=1
				student_obj.max_credit = 1.25*(add_credit+prev_sem_credit)/div
				student_obj.curr_registered_credits=0

				print(student_obj.total_credits)
				print(student_obj.cgpa)
				print(student_obj.max_credit)
				student_obj.save()
			for stu in student_objs:
				if(updated_year==curr_year+1):
					y = stu.current_year
					stu.current_year = y+1
				stu.current_sem = updated_sem
				stu.save()
			for curr in current_objs:
				curr.current_sem=updated_sem
				curr.current_year= updated_year
				curr.save()
			global good_message
			good_message = "Year,semester and  cgpa updated!!"
			return redirect('/dean_staff_office/update_sem_year_form')
		else:
			print("no")
			global error_message
			error_message = "Update only by 1 year!!!"
			return redirect('/dean_staff_office/update_sem_year_form/')
	
	else:
		return redirect('/dean_staff_office')
	
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


def portal_open_close(request):
	if request.session.has_key('staff_id'):
		template = loader.get_template('dean_staff_office/portal_open_close.html')
		portal_open_close_objs = portalsOpen.objects.all()
		crp_open = False
		grade_update_open = False
		global good_message
		for portal_open_close_obj in portal_open_close_objs:
			crp_open = portal_open_close_obj.crp_open
			grade_update_open = portal_open_close_obj.grade_update_open
		context = {'good_message':good_message, 'crp_open':crp_open, 'grade_update_open':grade_update_open}
		good_message = ''
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dean_staff_office/')

def portals_post(request):
	if request.session.has_key('staff_id'):
		if request.method=="POST":
			crp_open_list = request.POST.getlist('id_crp_open')
			print('crp_open_list=', crp_open_list)
			grade_update_open_list = request.POST.getlist('id_grade_open')
			print(grade_update_open_list)
			if not crp_open_list:
				crp_open = False
			else:
				crp_open = True
			if not grade_update_open_list:
				grade_update_open = False
			else:
				grade_update_open = True
			portal_open_close_objs = portalsOpen.objects.all()
			for portal_open_close_obj in portal_open_close_objs:
				portal_open_close_obj.crp_open = crp_open
				portal_open_close_obj.grade_update_open = grade_update_open
				portal_open_close_obj.save()
			global good_message
			good_message = 'Portal Updated succesfully!!'
			if crp_open == False:
				update_courses_students()
			return redirect('/dean_staff_office/portal_open_close')
		else:
			return redirect('/dean_staff_office/')
	else:
		return redirect('/dean_staff_office/')

def update_courses_students():
	student_objs = student.objects.all()
	for student_obj in student_objs:
		token_objs = token.objects.filter(student_obj = student_obj).delete()
		successfull_register_objs = successfull_register.objects.filter(student_id=student_obj)
		for successfull_register_obj in successfull_register_objs:
			takes_obj = takes(student_obj = student_obj, teaches = successfull_register_obj.teaches)
			takes_obj.save()
			successfull_register_obj.delete()

def add_dean(request):
	if request.session.has_key('staff_id'):
		template =loader.get_template('dean_staff_office/add_dean.html')
		context = {}
		faculty_obj=faculty.objects.all()
		global error_message
		
		global good_message
		
		context = {'faculty_obj':faculty_obj,'error_message':error_message,'good_message':good_message}
		error_message=''
		good_message=''
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/dean_staff_office/')

def dean_db(request):
	global error_message
	
	global good_message
	
	if request.session.has_key('staff_id'):
		faculty_id=request.POST['faculty']
		faculty_obj=faculty.objects.get(faculty_id=faculty_id)
		dean_obj=dean.objects.all()
		if dean_obj is not None:
			for deans in dean_obj:
				deans.delete()
		good_message='Added succesfully'
		dean_obj = dean(faculty_id=faculty_obj)
		dean_obj.save()
		return redirect('/dean_staff_office/add_dean')
					
					
		
	else:
		return redirect('/dean_staff_office/')


