# urls that start with gradinator will be handled here
from django.conf.urls import url
from gradinator import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^$', views.about_us, name='about_us'),
    url(r'^$', views.contact_us, name='contact_us'),
    url(r'^$', views.account, name='account'),
    url(r'^$', views.my_courses, name='my_courses'),
    url(r'^$', views.band_calculator, name='band_calculator'),
    url(r'^$', views.gpa_calculator, name='gpa_calculator'),

    #matches a course name
    url(r'^course/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='show_course'),

]
