from __future__ import unicode_literals
from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class department(models.Model):
	dept_id=models.CharField(max_length=25,primary_key=True)
	dept_name=models.CharField(max_length=25)
	def __str__(self):
   		return self.dept_name

class batch(models.Model):
	dept=models.ForeignKey(department)
	year=models.IntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)])
	def __str__(self):
		return self.dept.dept_name + " " + str(self.year)

class student(models.Model):
	student_id=models.CharField(max_length=25,primary_key=True)
	name=models.CharField(max_length=40)
	dept_id=models.ForeignKey(department,on_delete=models.CASCADE)
	cgpa=models.DecimalField(decimal_places=2,max_digits=3)
	curr_registered_credits=models.IntegerField()
	max_credit=models.IntegerField()
	total_credits=models.IntegerField()
	current_year=models.IntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)])
	current_sem=models.IntegerField(validators=[MaxValueValidator(2),MinValueValidator(1)])
	password=models.CharField(max_length=12)
	section_id=models.CharField(max_length=25, default='A')
	
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
	password=models.CharField(max_length=12)
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
	dateto=models.DateField()
	datefrom=models.DateField()
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	class Meta:
		unique_together=('dateto','datefrom','faculty_id')
	def __str__(self):
   		return self.faculty_id.name


class hod(models.Model):
	dateto=models.DateField()
	datefrom=models.DateField()
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	class Meta:
		unique_together=('dateto','datefrom','faculty_id')
	def __str__(self):
   		return self.faculty_id.name


class advisor(models.Model):
	year=models.IntegerField()
	batch=models.CharField(max_length=25)
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	class Meta:
		unique_together=('faculty_id','year')
	def __str__(self):
   		return self.faculty_id.name



class related(models.Model):
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	staff_id=models.ForeignKey(dean_staff_office,on_delete=models.CASCADE)
	dateto=models.DateField()
	datefrom=models.DateField()
	class Meta:
		unique_together=('staff_id','dateto','datefrom')
	def __str__(self):
   		return self.faculty_id.name + "  " + self.staff_id.staff_name
	
class teaches(models.Model):
	faculty_id=models.ForeignKey(faculty,on_delete=models.CASCADE)
	course_id=models.ForeignKey(course,on_delete=models.CASCADE)
	section_id=models.CharField(max_length=25)
	semester=models.IntegerField(default=1, validators=[MaxValueValidator(2),MinValueValidator(1)])
	year=models.IntegerField()
	slot=models.CharField(max_length=2)
	min_cgpa_constraint=models.DecimalField(decimal_places=2,max_digits=3)
	batch = models.ManyToManyField(batch)
	class Meta:
		unique_together=('faculty_id','section_id','course_id','semester','year','slot')
	def __str__(self):
   		return self.faculty_id.name + " " + self.course_id.course_id

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
	status=models.TextField()


	class Meta:
		unique_together=('student_obj','teaches')
	def __str__(self):
   		return self.student_id.name + " " + self.teaches.faculty_id.name + " " + self.teaches.course_id.title

class grades(models.Model):
	student_id=models.ForeignKey(student,on_delete=models.CASCADE)
	teaches=models.ForeignKey(teaches,on_delete=models.CASCADE)
	grade=models.CharField(max_length=2)
	def __str__(self):
   		return self.student_id.name + " " + self.teaches.faculty_id.name + " " + self.teaches.course_id.title




