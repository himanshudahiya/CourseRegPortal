from . import views
from django.conf.urls import url

app_name = 'dean_staff_office'

urlpatterns=[
	url('^$', views.index, name='index'),
	url('^logout/$', views.logout_user, name='logout'),
	url('^home/$', views.home, name='home'),
	url('^login/$', views.login_user, name='login'),
	url('^course_catalogue/', views.course_catalogue, name='course_catalogue'),
	url('^add_course', views.add_course, name='add_course'),
	url('^course_post', views.course_post, name='course_post')
]