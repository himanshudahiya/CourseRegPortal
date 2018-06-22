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
	if request.session.has_key('dean_id'):
		del request.session['dean_id']
	return redirect('/facultyportal/')

def update_cgpa(request):
    if request.session.has_key('faculty_id'):
        student_all = student.objects.all()

        for student_obj in student_all:
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
        	sums = (sums + prev_cgpa*student_obj.total_credits)/(student_obj.total_credits+add_credit)
        	student_obj.total_credits = student_obj.total_credits+add_credit
        	student_obj.cgpa =  sums
        	div=2
        	if student_obj.current_year==1 and student_obj.current_sem==1:
        		div=1
        	student_obj.max_credit = 1.25*(add_credit+prev_sem_credit)/div
        	student_obj.save()
    return redirect('/facultyportal/home')





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
		dean_list = dean.objects.all()
		is_dean = False
		for h in dean_list:
			if(h.faculty_id == faculty_obj):
				d = faculty_obj.dept_id
				is_dean = True				
				
		if is_dean:
			request.session['dean_id'] = faculty_id

	#		for batch in takes_t.teaches.batch.all():
	#			years.append(batch.year)
	#	context = {'faculty_obj':faculty_obj,'takes_obj':takes_obj, 'years': years}
		context = {'is_dean':is_dean,'faculty_obj':faculty_obj,'teaches_obj':teaches_obj,'current_year':current_year,'current_sem':current_sem}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/facultyportal/')

def grade(request, course_id):
	if request.session.has_key('faculty_id'):
		faculty_id=request.session['faculty_id']
		template = loader.get_template('facultyportal/grade.html')
		# faculty_id=faculty.objects.filter(faculty_id=faculty_id)
		faculty_obj = faculty.objects.get(faculty_id=faculty_id)
		current_obj = current.objects.all()
		for obj in current_obj:
			current_year=obj.current_year
			current_sem=obj.current_sem

		teaches_obj=teaches.objects.get(faculty_id=faculty_id,year=current_year,semester=current_sem,course_id=course_id)
		takes_obj = takes.objects.filter(teaches=teaches_obj)
		
		grades_list = ['--', '10', '9', '8', '7', '6', '5', '4', '0']

		student_grade_exist_list = []
		student_grade_not_exist_list =[]
		for students in takes_obj:
			if grades.objects.filter(student_id = students.student_obj, teaches = teaches_obj).exists():
				student_grade_exist_list.append(grades.objects.get(student_id = students.student_obj, teaches = teaches_obj))
			else:
				student_grade_not_exist_list.append(students)
		portal_objs = portalsOpen.objects.all()
		grade_update_open = False
		for portal_obj in portal_objs:
			grade_update_open = portal_obj.grade_update_open
	#		for batch in takes_t.teaches.batch.all():
	#			years.append(batch.year)
	#	context = {'faculty_obj':faculty_obj,'takes_obj':takes_obj, 'years': years}


		# <!-- {% if student_n.student_obj in student_grade_exist_list%} -->
  #               <!-- <option value="{{student_grades_list.objects.get(student_id = student_n.student_obj).grade}}">{{student_grades_list.objects.get(student_id = student_n.student_obj).grade}}</option>
  #           {% else %} -->
		context = {
			'faculty_obj':faculty_obj,
			'grades_list': grades_list, 
			'grade_update_open': grade_update_open, 
			'student_grade_exist_list':student_grade_exist_list,
			'student_grade_not_exist_list':student_grade_not_exist_list,
		}

		return HttpResponse(template.render(context,request))
	else:
		return redirect('/facultyportal/')
		
def update_grade(request,student_id,course_id):
	if request.session.has_key('faculty_id'):
		faculty_id=request.session['faculty_id']

		grade=request.POST['grade']
		print(student_id)
		print(course_id)
		print(grade)
		
		student_obj=student.objects.get(student_id=student_id)
		current_obj = current.objects.all()
		for obj in current_obj:
			current_year=obj.current_year
			current_sem=obj.current_sem
		teaches_obj=teaches.objects.get(faculty_id=faculty_id,year=current_year,semester=current_sem,course_id=course_id)
		if grades.objects.filter(student_id=student_obj,teaches=teaches_obj).exists():
			grade_obj = grades.objects.get(student_id=student_obj,teaches=teaches_obj)
			grade_obj.grade=grade

		else:
			grade_obj = grades(student_id=student_obj,teaches=teaches_obj,grade=grade)
		grade_obj.save()
			

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
		courses_not_floated = []
		for c in c_dept:
			if(not teaches.objects.filter(course_id = c.course_id , faculty_id = faculty_id, semester = current_sem, year = current_year).exists()):
				courses_not_floated.append(c)
			courses_of_dept.append(c)
	
		context = {'courses_of_dept':courses_of_dept, 
					'courses_not_floated':courses_not_floated,
				   'batch_obj':batch_obj
			
		}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('/facultyportal/')


def add_course_float(request):
	if request.session.has_key('faculty_id'):
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
			if b != course_id:
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
	else:
		return redirect('/facultyportal/')


def view_tokens(request):
	if request.session.has_key('faculty_id'):
		faculty_id = request.session['faculty_id']
		faculty_obj = faculty.objects.get(faculty_id = faculty_id)
		current_objs = current.objects.all()
		for current_obj in current_objs:
			current_year = current_obj.current_year
			current_sem = current_obj.current_sem


		teaches_course_tokens = []
		teaches_obj = teaches.objects.filter(faculty_id = faculty_obj, year = current_year, semester = current_sem)
		for teaches_tt in teaches_obj:
			teaches_courses = token.objects.filter(teaches = teaches_tt,status = 1)
			for teaches_course in teaches_courses:
				teaches_course_tokens.append(teaches_course)


		hod_list = hod.objects.all()
		hod_course = token.objects.filter(status = 2)
	

		for h in hod_list:
			if(h.faculty_id == faculty_obj):
				d = faculty_obj.dept_id				
				for i in hod_course:
					if (i.student_obj.dept_id==d):
						teaches_course_tokens.append(i)

		dean_list = dean.objects.all()
		dean_course = token.objects.filter(status = 3)
	
		is_dean = False
		for h in dean_list:
			if(h.faculty_id == faculty_obj):
				d = faculty_obj.dept_id
				is_dean = True				
				for i in dean_course:
					teaches_course_tokens.append(i)



		template = loader.get_template('facultyportal/token.html')
		context = {'teaches_course_tokens': teaches_course_tokens, 'is_dean':is_dean}
		return HttpResponse(template.render(context,request))

	else:
		return redirect('/facultyportal/')


def accept_close(request):
	if request.session.has_key('faculty_id'):
		faculty_id = request.session['faculty_id']
		if request.method =="POST":
			print("yesssss")
			request_value = request.POST['accept_close']
			request_value_att = request_value.split('+')
			student_id = request_value_att[0]
			course_id = request_value_att[1]
			semester = int(request_value_att[2])
			year = int(request_value_att[3])
			facl = request_value_att[4]
			student_obj = student.objects.get(student_id = student_id)
			course_obj = course.objects.get(course_id = course_id)	
			faculty_obj = faculty.objects.get(faculty_id = facl)
			teaches_obj = teaches.objects.get(faculty_id = faculty_obj, course_id = course_obj, semester = semester, year = year)
			token_obj = token.objects.get(student_obj = student_obj, teaches = teaches_obj).delete()
			takes_obj = successfull_register(student_id = student_obj, teaches = teaches_obj)
			takes_obj.save()
			course_credit = 0
			n = int(course_obj.credit_struct)
			while n:
				course_credit, n = course_credit + n % 10, n // 10
			student_obj.curr_registered_credits = student_obj.curr_registered_credits + course_credit
			student_obj.save()
			return redirect('/facultyportal/view_tokens/')
		else:
			return redirect('/facultyportal/')
	else:
		return redirect('/facultyportal/')

def reject_close(request):
	if request.session.has_key('faculty_id'):
		if request.method =="POST":
			request_value = request.POST['reject_close']
			request_value_att = request_value.split('+')
			student_id = request_value_att[0]
			course_id = request_value_att[1]
			semester = int(request_value_att[2])
			year = int(request_value_att[3])
			facl = request_value_att[4]
			student_obj = student.objects.get(student_id = student_id)
			course_obj = course.objects.get(course_id = course_id)
			faculty_obj = faculty.objects.get(faculty_id = facl)
			teaches_obj = teaches.objects.get(faculty_id = faculty_obj, course_id = course_obj, semester = semester, year = year)
			token_obj = token.objects.get(student_obj = student_obj, teaches = teaches_obj).delete()
			return redirect('/facultyportal/view_tokens/')
		else:
			return redirect('/facultyportal/')
	else:
		return redirect('/facultyportal/')


def accept_pass(request):
	if request.session.has_key('faculty_id'):
		if request.method =="POST":
			request_value = request.POST['accept_pass']
			request_value_att = request_value.split('+')
			student_id = request_value_att[0]
			course_id = request_value_att[1]
			semester = int(request_value_att[2])
			year = int(request_value_att[3])
			student_obj = student.objects.get(student_id = student_id)
			course_obj = course.objects.get(course_id = course_id)
			facl= request_value_att[4]
			faculty_obj = faculty.objects.get(faculty_id = facl)
			teaches_obj = teaches.objects.get(faculty_id = faculty_obj, course_id = course_obj, semester = semester, year = year)
			token_obj = token.objects.get(student_obj = student_obj, teaches = teaches_obj)
			token_obj.status = token_obj.status + 1
			token_obj.save()

			return redirect('/facultyportal/view_tokens/')
		else:
			return redirect('/facultyportal/')
	else:
		return redirect('/facultyportal/')