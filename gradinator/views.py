from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import HttpResponse

from gradinator.models import UserGrade
from gradinator.models import UserProfile
from gradinator.models import Course
from gradinator.models import Coursework
from gradinator.models import UserCourseworkGrade

from gradinator.forms import UserProfileForm
from gradinator.forms import UserGradeForm

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
    # a view that shows all courses that the current user has enrolled in
    username = get_username(request)
    # a list of objects that are the courses the current user
    # is enrolled in and their grade
    users_grades = UserGrade.objects.filter(sat_by=username)

    course_list = []
    for grade in users_grades:
        course_list.append(grade.grade_for)

    context_dict = {'my_courses': course_list}

    return render(request, 'gradinator/my_courses.html', context_dict)


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
def enrol(request, course_name_slug=""):
    # should show all courses where the user has not already enrolled in
    # ordered by year then by school ie school of computer science [needs discussion]
    # then lets users add courses to their account
    user = UserProfile.objects.get(user=request.user)
    users_course_list = UserGrade.objects.filter(sat_by=user)

    all_courses = Course.objects.filter()
    to_exclude = []
    for any_course in all_courses:
        for user_course in users_course_list:
            if any_course == user_course.grade_for:
                to_exclude.append(any_course.id)

    not_enrolled = Course.objects.exclude(id__in=to_exclude)
    context_dict = {'not_enrolled': not_enrolled}

    form = UserGrade()
    if request.method == 'POST':
        form = UserGradeForm(request.POST, request.FILES)
        course = Course.objects.get(slug=course_name_slug)
        if form.is_valid() and course:
            user_grade = form.save(commit=False)
            user_grade.sat_by = UserProfile.objects.get(user=request.user)
            user_grade.grade_for = course
            user_grade.save()
            return HttpResponse()
        else:
            print(form.errors)
            if course is None:
                print(course)
    context_dict['form'] = form
    # functionality to search for a course not tested yet
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


@login_required
def band_calculator(request):
    # context dictionary should contain a dictionary that contains all of the courses the user sits
    # with the associated coursework for that course
    username = get_username(request)

    # a list of objects that are the courses the current user
    # is enrolled in and their grade
    users_grades = UserGrade.objects.filter(sat_by=username)

    # all courses sat by user
    # they are course objects not names of courses
    course_list = []
    for grade in users_grades:
        course_list.append(grade.grade_for)

    associated_coursework = []
    for index_course in course_list:
        # adds the coursework associated with each users course into  a dictionary
        associated_coursework.append((index_course, Coursework.objects.filter(course=index_course)))
    # a dictionary with values being dictionaries containing each users courses' coursework
    # coursework_grades = UserCourseworkGrade.objects.filter(coursework_for__in=associated_coursework)

    context_dict = {'my_courses': course_list, 'coursework_grades': associated_coursework}
    return render(request, 'gradinator/band_calculator.html', context_dict)


@login_required
def add_user_coursework(request, coursework_slug):
    # context dictionary should contain a dictionary that contains all of the courses the user sits
    # with the associated coursework for that course
    username = get_username(request)

    # a list of objects that are the courses the current user
    # is enrolled in and their grade
    users_grades = UserGrade.objects.filter(sat_by=username)

    # all courses sat by user
    # they are course objects not names of courses
    course_list = []
    for grade in users_grades:
        course_list.append(grade.grade_for)

    associated_coursework = []
    for index_course in course_list:
        # adds the coursework associated with each users course into  a dictionary
        associated_coursework.append((index_course, Coursework.objects.filter(course=index_course)))

    context_dict = {'my_courses': course_list, 'coursework_grades': associated_coursework}

    form = UserGrade()
    if request.method == 'POST':
        form = UserGradeForm(request.POST, request.FILES)
        course = Course.objects.get(slug=coursework_slug)
        if form.is_valid() and course:
            user_grade = form.save(commit=False)
            user_grade.sat_by = UserProfile.objects.get(user=request.user)
            user_grade.grade_for = course
            user_grade.save()
            return HttpResponse()
        else:
            print(form.errors)
            if course is None:
                print("here")
    context_dict['form'] = form
    return render(request, 'gradinator/band_calculator.html', context_dict)


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
    user = UserProfile.objects.get(user=request.user)
    return user


def create_user_profile():
    # helper function that creates the user profile objects
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


@login_required
def register_profile(request):
    create_user_profile()
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
