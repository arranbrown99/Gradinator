from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gradinator.models import UserGrade
from gradinator.models import User
from gradinator.models import Course
from gradinator.models import CourseWork

#from rango.webhose_search import run_query
import rango.webhose_search


# Create your views here.
@login_required
def home(request):
    context_dict = {}
    return render(request, 'gradinator/home.html', context_dict)


@login_required
def account(request):
    # view that shows the current users information
    username = get_username(request)
    # userInformation contains fields; GUID, Password, picture, email and GPA
    user_information = User.objects.filter(GUID=username)
    context_dict = {'user': user_information}

    return render(request, 'gradinator/account.html', context_dict)


@login_required
def my_courses(request):
    # a view that shows all courses that the current user has enrolled in
    username = get_username(request)
    # if user is logged in
    if username is not None:
        # a list of objects that are the courses the current user
        # is enrolled in and their grade
        course_list = UserGrade.objects.filter(SatBy=username)
        context_dict = {'my_courses': course_list}
    else:
        # if not logged in no courses
        # might need to change this
        course_list = None
        context_dict = {'my_courses': course_list}
    return render(request, 'gradinator/my_courses.html', context_dict)


@login_required
def show_course(request, course_name_slug):
    context_dict = {}
    try:
        # Can we find a course name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        course = Course.objects.get(slug=course_name_slug)
        context_dict['category'] = course
    except Course.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['course'] = None

    # Go render the response and return it to the client.
    return render(request, 'gradinator/course.html', context_dict)


@login_required
def enrol(request):
    # should show all courses where the user has not already enrolled in
    # ordered by year then by school ie school of computer science [needs discussion]
    # then lets users add courses to their account
    username = get_username(request)
    users_course_list = UserGrade.objects.filter(SatBy=username)

    # should get all courses the user is not currently enrolled in
    names_users_course = []
    counter = 0
    for course in users_course_list:
        names_users_course[counter] = course.GradeFor
        counter += 1

    # still needs to be ordered
    not_enrolled = Course.objects.exclude(ID__in=names_users_course)

    context_dict = {'not_enrolled': not_enrolled}

    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Webhose search function to get the results list!
            result_list = run_query(query)
    course_dict = {'result_list': result_list}

    return render(request, 'gradinator/enrol.html', context_dict)


@login_required
def about_us(request):
    context_dict = {}
    return render(request, 'gradinator/about_us.html', context_dict)


@login_required
def contact_us(request):
    context_dict = {}
    return render(request, 'gradinator/contact_us.html', context_dict)


@login_required
def search(request):
    context_dict = {}
    return render(request, 'gradinator/search.html', context_dict)


@login_required
def band_calculator(request):
    # context dictionary should contain a dictionary that contains all of the courses the user sits
    # with the associated coursework for that course
    username = get_username(request)
    # all courses sat by user
    # they are course objects not names of courses
    course_list = UserGrade.objects.filter(SatBy=username)
    associated_coursework = {}
    for index_course in course_list:
        # adds the coursework associated with each users course into  a dictionary
        associated_coursework[index_course] = Coursework.objects.filter(Course=index_course.ID)
    # a dictionary with values being dictionaries containing each users courses' coursework
    context_dict = {'my_courses': associated_coursework}
    return render(request, 'gradinator/band_calculator.html', context_dict)


@login_required
def gpa_calculator(request):
    # view returns the object of the current user which contains a field called GPA
    # which  is not physically calculated here but by the model
    username = get_username(request)

    context_dict = {'user': User.objects.filter(GUID=username)}
    return render(request, 'gradinator/gpa_calculator.html', context_dict)


def get_username(request):
    # helper function that gets the username if the user is logged in
    if request.user.is_authenticated():
        username = request.user.username
        return username
    else:
        return None


