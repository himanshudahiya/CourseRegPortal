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
	url('^course_post', views.course_post, name='course_post'),
	url('^edit_course/(?P<course_id>[A-Za-z]*[0-9]+)', views.edit_course, name='edit_course'),
	url('^course_edit_post/(?P<course_id_prev>[A-Za-z]*[0-9]+)', views.course_edit_post, name='course_edit_post'),
	url('^student_catalogue', views.student_catalogue, name='student_catalogue'),
	url('^add_student', views.add_student, name='add_student'),
	url('^student_post', views.student_post, name='student_post'),
	url('^edit_student/(?P<student_id>[A-Za-z]*[0-9]+)', views.edit_student, name='edit_student'),
	url('^student_edit_post/(?P<student_id_prev>[A-Za-z]*[0-9]+)', views.student_edit_post, name='student_edit_post'),
	url('^add_hod', views.add_hod, name='add_hod'),
	url('^hod_db', views.hod_db, name='hod_db'),
	url('^add_advisor', views.add_advisor, name='add_advisor'),
	url('^advisor_db', views.advisor_db, name='advisor_db'),
	url('^update_sem_year_form' , views.update_sem_year_form , name = 'update_sem_year_form'),
	url('^update_sem_year' , views.update_sem_year , name = 'update_sem_year'),
	url('^faculty_catalogue/', views.faculty_catalogue, name='faculty_catalogue'),
	url('^add_faculty', views.add_faculty, name='add_faculty'),
	url('^faculty_post', views.faculty_post, name='faculty_post'),
	url('^edit_faculty/(?P<faculty_id>[A-Za-z]*[0-9]+)', views.edit_faculty, name='edit_faculty'),
	url('^faculty_edit_post/(?P<faculty_id_prev>[A-Za-z]*[0-9]+)', views.faculty_edit_post, name='faculty_edit_post'),
	url('^portal_open_close/', views.portal_open_close, name='portal_open_close'),
	url('^portals_post/', views.portals_post, name='portals_post'),
	url('^add_dean/', views.add_dean, name='add_dean'),
	url('^dean_db/', views.dean_db, name='dean_db')
]
