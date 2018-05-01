from . import views
from django.conf.urls import url


app_name = 'studentportal'

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^view_grades', views.view_grades, name='view_grades'),
	url('^logout/$', views.logout_user, name='logout'),
	url('^home/$', views.home, name='home'),
	url('^login/$', views.login_user, name='login'),
	url('^register_courses/$', views.register_courses, name='register_courses'),
	url('^add_course_batch/$', views.add_course_batch, name='add_course_batch'),
	url('^add_course_other_batch/$', views.add_course_other_batch, name='add_course_other_batch'),
	url('^delete_reg_course', views.delete_reg_course, name='delete_reg_course'),
	url('^delete_tokened_course', views.delete_tokened_course, name='delete_tokened_course')
]