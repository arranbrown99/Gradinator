from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import redirect

from gradinator.models import UserGrade
from gradinator.models import UserProfile
from gradinator.models import Course
from gradinator.models import Coursework
from gradinator.models import UserCourseworkGrade

from gradinator.forms import UserProfileForm

from gradinator.webhose_search import run_query


# Create your views here.
@login_required
def home(request):
    context_dict = {}
    return render(request, 'gradinator/home.html', context_dict)


@login_required
def faq(request):
    context_dict = {}
    return render(request, 'gradinator/faq.html', context_dict)


@login_required
def account(request, username):
    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return redirect('index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'email': userprofile.email, 'picture': userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('account', user.username)
        else:
            print(form.errors)
    return render(request, 'gradinator/account.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def my_courses(request):
    #     # a view that shows all courses that the current user has enrolled in
    #     username = get_username(request)
    #     # if user is logged in
    #     if username is not None:
    #         # a list of objects that are the courses the current user
    #         # is enrolled in and their grade
    #         course_list = UserGrade.objects.filter(SatBy=username)
    #         context_dict = {'my_courses': course_list}
    #     else:
    #         # if not logged in no courses
    #         # might need to change this
    #         course_list = None
    #         context_dict = {'my_courses': course_list}
    return render(request, 'gradinator/my_courses.html', {})


@login_required
def show_course(request, course_name_slug):
    context_dict = {}
    try:
        # Can we find a course name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        course = get_object_or_404(Course, slug=course_name_slug)
        # course = Course.objects.get(slug=course_name_slug)
        context_dict['course'] = course

        # functionality to update the current grade for each coursework associated with the course
        coursework = Coursework.objects.filter(course=course)
        context_dict['coursework'] = coursework

    except Course.DoesNotExist:
        # We get here if we didn't find the specified course.
        # Don't do anything -
        # the template will display the "no course" message for us.
        context_dict['course'] = None

    # Go render the response and return it to the client.
    return render(request, 'gradinator/course.html', context_dict)


@login_required
def enrol(request):
    # should show all courses where the user has not already enrolled in
    # ordered by year then by school ie school of computer science [needs discussion]
    # then lets users add courses to their account
    username = get_username(request)
    users_course_list = UserGrade.objects.filter(sat_by=username)

    # should get all courses the user is not currently enrolled in
    names_users_course = []
    counter = 0
    for course in users_course_list:
        names_users_course[counter] = course.GradeFor
        counter += 1

    # still needs to be ordered
    not_enrolled = Course.objects.exclude(id__in=names_users_course)

    context_dict = {'not_enrolled': not_enrolled}

    # result_list = []
    # if request.method == 'POST':
    #     query = request.POST['query'].strip()
    #     if query:
    #         # Run our Webhose search function to get the results list!
    #         result_list = run_query(query)
    # context_dict['result_list'] = result_list

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


#
# @login_required
# def band_calculator(request):
#     # context dictionary should contain a dictionary that contains all of the courses the user sits
#     # with the associated coursework for that course
#     username = get_username(request)
#     # all courses sat by user
#     # they are course objects not names of courses
#     course_list = UserGrade.objects.filter(SatBy=username)
#     associated_coursework = {}
#     for index_course in course_list:
#         # adds the coursework associated with each users course into  a dictionary
#         associated_coursework[index_course] = Coursework.objects.filter(Course=index_course.ID)
#     # a dictionary with values being dictionaries containing each users courses' coursework
#     coursework_grades = UserCourseworkGrade.objects.filter(coursework_for__in=associated_coursework)
#     context_dict = {'my_courses': course_list, 'coursework_grades': coursework_grades}
#     return render(request, 'gradinator/band_calculator.html', context_dict)
#
#
# @login_required
# def gpa_calculator(request):
#     # view returns the object of the current user which contains a field called GPA
#     # which  is not physically calculated here but by the model
#     username = get_username(request)
#
#     context_dict = {'user': User.objects.filter(GUID=username)}
#     return render(request, 'gradinator/gpa_calculator.html', context_dict)


def get_username(request):
    # helper function that gets the username if the user is logged in
    if request.user.is_authenticated():
        username = request.user.username
        return username
    else:
        return None


def create_user_profile():
    # helper function that creates the user profile objects
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'gradinator/profile_registration.html', context_dict)
