from __future__ import unicode_literals
from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
# Create your models here.
now = datetime.datetime.now()
class department(models.Model):
	dept_id=models.IntegerField()
	dept_name=models.CharField(max_length=25)
	def __str__(self):
   		return self.dept_name

class batch(models.Model):
	dept=models.ForeignKey(department,on_delete=models.CASCADE)
	year=models.IntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)])
	def __str__(self):
		return self.dept.dept_name + " " + str(self.year)


class student(models.Model):
	student_id=models.CharField(max_length=25,primary_key=True)
	name=models.CharField(max_length=40)
	dept_id=models.ForeignKey(department,on_delete=models.CASCADE)
	cgpa=models.DecimalField(decimal_places=2,max_digits=10,default=0)
	curr_registered_credits=models.IntegerField(default=0)
	max_credit=models.DecimalField(default=24, max_digits=10, decimal_places=2)
	total_credits=models.DecimalField(default=0, max_digits=10, decimal_places=2)
	current_year=models.IntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)],default=1)
	current_sem=models.IntegerField(validators=[MaxValueValidator(2),MinValueValidator(1)],default=1)
	password=models.CharField(max_length=50,default="abcdefgh")
	student_email=models.CharField(max_length=100, default="")	
	def __str__(self):
   		return self.name


class course(models.Model):
	course_id=models.CharField(max_length=25,primary_key=True)
	credit_struct=models.CharField(max_length=25)
	title=models.CharField(max_length=40)
	dept_id=models.ForeignKey(department,on_delete=models.CASCADE)
	def __str__(self):
   		return self.title


class faculty(models.Model):
	faculty_id=models.CharField(max_length=25,primary_key=True)
	name=models.CharField(max_length=40)
	dept_id=models.ForeignKey(department,on_delete=models.CASCADE)
	password=models.CharField(max_length=12, default="abcdefgh")
	email_id=models.EmailField()
	def __str__(self):
   		return self.name

class dean_staff_office(models.Model):
	staff_id=models.CharField(max_length=25,primary_key=True)
	staff_name=models.CharField(max_length=40)
	password=models.CharField(max_length=12)
	email_id=models.EmailField()
	def __str__(self):
   		return self.staff_name

class dean(models.Model):
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	def __str__(self):
   		return self.faculty_id.name


class hod(models.Model):
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	def __str__(self):
   		return self.faculty_id.name


class advisor(models.Model):
	batch=models.ForeignKey(batch,on_delete=models.CASCADE)
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	class Meta:
		unique_together=('faculty_id','batch')
	def __str__(self):
   		return self.faculty_id.name
	
class teaches(models.Model):
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	course_id=models.ForeignKey(course,on_delete=models.CASCADE)
	semester=models.IntegerField(default=1, validators=[MaxValueValidator(2),MinValueValidator(1)])
	year=models.IntegerField()
	slot=models.CharField(max_length=2)
	min_cgpa_constraint=models.DecimalField(decimal_places=2,max_digits=3)
	batch = models.ManyToManyField(batch)
	prerequisite = models.ManyToManyField(course, related_name = "prerequisites", null=True, blank=True)
	class Meta:
		unique_together=('faculty_id','course_id','semester','year','slot')
	def __str__(self):
   		return self.course_id.title + " " + self.course_id.course_id

class takes(models.Model):
	student_obj=models.ForeignKey(student,on_delete=models.CASCADE)
	teaches=models.ForeignKey(teaches,on_delete=models.CASCADE)
	class Meta:
		unique_together=('student_obj','teaches')
	def __str__(self):
   		return self.student_obj.name + " " + self.teaches.faculty_id.name + " " + self.teaches.course_id.title

class successfull_register(models.Model):
	student_id=models.ForeignKey(student,on_delete=models.CASCADE)
	teaches=models.ForeignKey(teaches,on_delete=models.CASCADE)
	class Meta:
		unique_together=('student_id','teaches')
	def __str__(self):
   		return self.student_id.name + " " + self.teaches.faculty_id.name + " " + self.teaches.course_id.title

class token(models.Model):
	student_obj=models.ForeignKey(student,on_delete=models.CASCADE)
	teaches=models.ForeignKey(teaches,on_delete=models.CASCADE)
	status=models.IntegerField(default=1)
	reason=models.TextField(default = ":and:")

	class Meta:
		unique_together=('student_obj','teaches')
	def __str__(self):
   		return self.student_obj.name + " " + self.teaches.faculty_id.name + " " + self.teaches.course_id.title

class grades(models.Model):
	student_id=models.ForeignKey(student,on_delete=models.CASCADE)
	teaches=models.ForeignKey(teaches,on_delete=models.CASCADE)
	grade=models.CharField(max_length=2)
	def __str__(self):
   		return self.student_id.name + " " + self.teaches.faculty_id.name + " " + self.teaches.course_id.title


class current(models.Model):
	current_year = models.IntegerField(default=now.year)
	current_sem = models.IntegerField(default=1)
	def __str__(self):
		return str(self.current_year) + " " + str(self.current_sem)

class portalsOpen(models.Model):
	crp_open = models.BooleanField(default=False)
	grade_update_open = models.BooleanField(default=False)
	# crp_close=models.BooleanField(default=False)
	def __str__(self):
		return str(self.crp_open) +" " +str(self.grade_update_open)
