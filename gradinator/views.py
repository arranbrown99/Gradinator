from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response

import json
from gradinator.models import UserGrade
from gradinator.models import UserProfile
from gradinator.models import Course
from gradinator.models import Coursework
from gradinator.models import UserCourseworkGrade

from gradinator.forms import UserProfileForm
from gradinator.forms import UserGradeForm
from gradinator.forms import UserCourseworkGradeForm


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
    create_user_profile()
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
    create_user_profile()
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

    form = UserGradeForm()
    if request.method == 'POST':
        form = UserGradeForm(request.POST, request.FILES)
        course = Course.objects.get(slug=course_name_slug)
        if form.is_valid() and course:
            user_grade = form.save(commit=False)
            user_grade.sat_by = UserProfile.objects.get(user=request.user)
            user_grade.grade_for = course
            user_grade.save()
            return render(request, 'gradinator/enrol.html', context_dict)
        else:
            print(form.errors)

    context_dict['form'] = form

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
    # context dictionary should contain a dictionary that contains all of the coursework associated with each course
    #  the user takes only including coursework already added
    create_user_profile()
    username = get_username(request)
    users_courses = UserGrade.objects.filter(sat_by=username)

    users_courseworks = UserCourseworkGrade.objects.filter(sat_by=username)

    not_enrolled = {}

    appended = False
    for course in users_courses:
        c = course.grade_for
        users_cw = UserCourseworkGrade.objects.filter(sat_by=username)
        list_coursework = []

        for coursework in users_cw:
            if coursework.grade_for.course == c:
                list_coursework.append(coursework)

        # total weight of all coursework the user has sat so far
        weight_sat = 0
        for coursework in list_coursework:
            weight_sat += coursework.grade_for.weight

        # remaining weight of all coursework the user still has to sit
        # if it is 0 then all coursework will have been sat and their is nothing to predict
        remaining_weight = 100 - weight_sat
        if remaining_weight == 0:
            continue

        all_coursework = Coursework.objects.filter(course=course.grade_for)
        include = []
        for users_coursework in users_courseworks:
            for coursework in all_coursework:
                if users_coursework.grade_for == coursework:
                    appended = True
                    include.append(coursework)

        filtered = users_courseworks.filter(grade_for__in=include)
        not_enrolled[course.grade_for] = filtered

    if appended:
        context_dict = {}
        context_dict['not_enrolled'] = not_enrolled

    else:
        context_dict = {'not_enrolled': None}

    return render(request, 'gradinator/band_calculator.html', context_dict)


@login_required
def band_calculator_slug(request, course_name_slug):
    # should take in a course that a user sits and has entered coursework grades for
    # should output what the user needs to get in the remaining coursework to get each band

    username = get_username(request)
    course = Course.objects.get(slug=course_name_slug)
    users_coursework = UserCourseworkGrade.objects.filter(sat_by=username)
    list_coursework = []

    for coursework in users_coursework:
        if coursework.grade_for.course == course:
            list_coursework.append(coursework)

    # total weight of all coursework the user has sat so far
    weight_sat = 0
    for coursework in list_coursework:
        weight_sat += coursework.grade_for.weight

    # remaining weight of all coursework the user still has to sit
    remaining_weight = 100 - weight_sat
    if remaining_weight == 0:
        return band_calculator(request)
    context_dict = {"average_needed": {}}

    bands = {"A": {"A1": 92, "A2": 85, "A3": 79, "A4": 74, "A5": 70}, "B": {"B1": 67, "B2": 64, "B3": 60, },
             "C": {"C1": 57, "C2": 64, "C3": 50, }, "D": {"D1": 47, "D2": 44, "D3": 40, }}
    for string_grade, dict_grades in bands.items():
        context_dict["average_needed"][string_grade] = {}
        for band, grade in dict_grades.items():
            total_usersgrade = 0
            for coursework in list_coursework:
                total_usersgrade += coursework.grade * coursework.grade_for.weight / 100

            average_needed = (grade - total_usersgrade) * 100 / remaining_weight
            average_needed = round(average_needed, 2)
            context_dict["average_needed"][string_grade][band] = average_needed
    context_dict["course"] = course

    return render(request, 'gradinator/band_calculator_slug.html', context_dict)


@login_required
def add_user_coursework(request):
    # context dictionary should contain a dictionary that contains all of the coursework associated with each course
    #  the user takes not including coursework already added
    create_user_profile()
    username = get_username(request)
    users_courses = UserGrade.objects.filter(sat_by=username)

    users_courseworks = UserCourseworkGrade.objects.filter(sat_by=username)

    not_enrolled = {}
    for course in users_courses:
        all_coursework = Coursework.objects.filter(course=course.grade_for)
        exclude = []
        for users_coursework in users_courseworks:
            for coursework in all_coursework:
                if users_coursework.grade_for == coursework:
                    exclude.append(coursework.name)

        filtered = all_coursework.exclude(name__in=exclude)
        not_enrolled[course.grade_for] = filtered

    context_dict = {'not_enrolled': not_enrolled}

    return render(request, 'gradinator/add_user_coursework.html', context_dict)


def add_coursework_form(request, coursework_slug):
    # a form that creates a UserCourseWork grade model object
    form = UserCourseworkGradeForm()
    if request.method == 'POST':
        form = UserCourseworkGradeForm(request.POST, request.FILES)
        coursework = Coursework.objects.get(slug=coursework_slug)
        if form.is_valid() and coursework:

            user_grade = form.save(commit=False)
            user_grade.sat_by = UserProfile.objects.get(user=request.user)
            user_grade.grade_for = coursework
            user_grade.save()

            return add_user_coursework(request)
        else:
            print(form.errors)

    context_dict = {'form': form, "coursework": coursework_slug}
    return render(request, 'gradinator/add_coursework_form.html', context_dict)


@login_required
def gpa_calculator(request):
    # calculates the gpa using grade points

    list_completed_usergrade = load_usergrade(request)
    grade_points = {"A1": (92, 22), "A2": (85, 21), "A3": (79, 20), "A4": (74, 19), "A5": (70, 18),
                    "B1": (67, 17), "B2": (64, 16), "B3": (60, 15),
                    "C1": (57, 14), "C2": (54, 13), "C3": (50, 12),
                    "D1": (47, 11), "D2": (44, 10), "D3": (40, 9),
                    "E1": (37, 8), "E2": (34, 7), "E3": (30, 6),
                    "F1": (27, 5), "F2": (24, 4), "F3": (20, 3),
                    "G1": (15, 2), "G2": (10, 1), "H": (0, 0), "CW": (0, 0)}
    triple_completed_usergrade = []

    # calculates the grade point for a given grade
    # and the GPA
    gpa = 0
    total_credits = 0
    for usergrade in list_completed_usergrade:
        current_biggest = "A1"
        current_smallest = "CW"
        for key, value in grade_points.items():
            number = usergrade.grade
            if usergrade.grade >= value[0] and value[0] > grade_points[current_smallest][0]:
                current_smallest = key
            if usergrade.grade <= value[0] and value[0] < grade_points[current_biggest][0]:
                current_biggest = key

        triple_completed_usergrade.append((usergrade, current_biggest, grade_points[current_biggest]))

        gpa += grade_points[current_smallest][1] * usergrade.grade_for.credits
        total_credits += usergrade.grade_for.credits
    if total_credits == 0:
        context_dict = {"list": None, "gpa": None}
    else:
        gpa = gpa / total_credits
        gpa = round(gpa, 2)
        context_dict = {"list": triple_completed_usergrade, "gpa": gpa}
    return render(request, 'gradinator/gpa_calculator.html', context_dict)


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
    # adds a new user
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


def load_usergrade(request):
    # function that calculates a users grade for every course if they have completed every peice of coursework
    #  for that course
    create_user_profile()
    username = get_username(request)

    completed_user_courses = []
    usergrade = UserGrade.objects.filter(sat_by=username)
    users_coursework = UserCourseworkGrade.objects.filter(sat_by=username)

    for user_course in usergrade:

        # a list of all coursework associated with the current course
        list_coursework = []

        for coursework in users_coursework:
            if coursework.grade_for.course == user_course.grade_for:
                list_coursework.append(coursework)

        # if a user has done all coursework for a given course
        coursework_for_course = Coursework.objects.filter(course=user_course.grade_for)
        if len(coursework_for_course) == len(list_coursework):

            total_coursework_grade = 0
            for coursework in list_coursework:
                total_coursework_grade += (coursework.grade * coursework.grade_for.weight / 100)

            user_course.grade = total_coursework_grade
            user_course.save()
            completed_user_courses.append(user_course)

    return completed_user_courses
