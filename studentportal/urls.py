from . import views
from django.conf.urls import url


app_name = 'studentportal'

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^logout/', views.logout_user, name='logout'),
	url('^home/', views.home, name='home'),
	url('^login', views.login_user, name='login'),
	url('^register_courses', views.register_courses, name='register_courses'),
	url('^add_course_batch', views.add_course_batch, name='add_course_batch')
]