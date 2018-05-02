"""DBMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^register/', include('register.urls')),
    url('^studentportal/', include('studentportal.urls')),
    url('^facultyportal/', include('facultyportal.urls')),
<<<<<<< HEAD

    url('^dean_staff_office/',include('dean_staff_office.urls'))

=======
    url('^dean_staff_office/',include('dean_staff_office.urls'))
>>>>>>> ab407c8080b0c545ea56e0223813f3d042a3985a
]
