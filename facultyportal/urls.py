from . import views
from django.conf.urls import url


app_name = 'facultyportal'

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^logout/', views.logout_user, name='logout'),
	url('^home/', views.home, name='home'),
	url('^login', views.login_user, name='login'),
	url('^grade/(?P<course_id>[A-Za-z0-9]+)', views.grade, name='grade'),
	url('^update_grade/(?P<student_id>[A-Za-z0-9]+)/(?P<course_id>[A-Za-z0-9]+)', views.update_grade, name='update_grade'),
	url('^add_course_float', views.add_course_float, name='add_course_float'),

	url('^float_new_courses', views.float_new_courses, name='float_new_courses'),
	url('^view_tokens', views.view_tokens, name='view_tokens'),
	url('^accept_close', views.accept_close, name='accept_close'),
	url('^reject_close', views.reject_close, name='reject_close'),
	url('^accept_pass', views.accept_pass, name='accept_pass'),

	url('^update_cgpa', views.update_cgpa, name='update_cgpa'),

	]

