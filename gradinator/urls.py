# urls that start with gradinator will be handled here
from django.conf.urls import url
from gradinator import views

urlpatterns = [
    url(r'home/$', views.home, name='home'),
    url(r'about_us/$', views.about_us, name='about_us'),
    url(r'contact_us/$', views.contact_us, name='contact_us'),
    url(r'faq/$', views.faq, name='faq'),
    url(r'^account/(?P<username>[\w\-]+)/$', views.account, name='account'),

    url(r'my_courses/$', views.my_courses, name='my_courses'),
    url(r'enrol/$', views.enrol, name='enrol'),
    url(r'enrol/(?P<course_name_slug>[\w\-]+)/$', views.enrol, name='enrol'),

    url(r'band_calculator/$', views.band_calculator, name='band_calculator'),
    # url(r'gpa_calculator/$', views.gpa_calculator, name='gpa_calculator'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    # matches a course name
    url(r'^course/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='show_course'),

]
