from . import views
from django.conf.urls import url


app_name = 'studentportal'

urlpatterns = [
	url('^$', views.index, name='index'),
	url('^logout/', views.logout_user, name='logout'),
	url('^home/', views.home, name='home'),
	url('^login', views.login_user, name='login'),
]