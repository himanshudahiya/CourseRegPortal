from . import views
from django.conf.urls import url


app_name = 'register' 

urlpatterns = [
	url('^$', views.index, name='index'),
    url('^register/', views.UserFormView.as_view(), name='register'),
    url('^home/', views.home, name='home'),
    url('^logout/', views.logout_user, name='logout'),
    url('^login/', views.login_user, name='login'),
]