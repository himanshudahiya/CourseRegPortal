from . import views
from django.conf.urls import url


app_name = 'facultyportal'

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^logout/', views.logout_user, name='logout'),
	url('^home/', views.home, name='home'),
	url('^login', views.login_user, name='login'),
	url('^grade/(?P<course_id>[A-Za-z0-9]+)', views.grade, name='grade'),
 	url('^add_course_float', views.add_course_float, name='add_course_float'),
	url('^float_new_courses', views.float_new_courses, name='float_new_courses')
# 
]