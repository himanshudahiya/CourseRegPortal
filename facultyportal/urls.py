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

# 	url('^register_courses', views.register_courses, name='register_courses'),
# 	url('^add_course_batch', views.add_course_batch, name='add_course_batch')
# 
]