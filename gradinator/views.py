from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rango.models import UserGrade
from rango.models import User
from rango.models import Course



# Create your views here.
def home(request):
    context_dict = {}
    return render(request, 'gradinator/home.html', context_dict)


def signup(request):
    # taken from tango with django textbook
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context.

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'gradinator/signup.html', context_dict)


def login(request):
    context_dict = {}
    return render(request, 'gradinator/login.html', context_dict)


@login_required
def account(request):
    # view that shows the current users information
    context_dict = {}
    username = get_username(request)
    # userInformation contains fields; GUID, Password, picture, email and GPA
    user_information = User.objects.filter(GUID=username)
    context_dict = {'user': user_information}

    return render(request, 'gradinator/account.html', context_dict)


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


def show_course(request, course_name_slug):
    context_dict = {}
    try:
        # Can we find a course name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        course = Course.objects.get(slug=course_name_slug)
        context_dict['category'] = course
    except course.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['course'] = None

    # Go render the response and return it to the client.
    return render(request, 'gradinator/course.html', context_dict)


def about_us(request):
    context_dict = {}
    return render(request, 'gradinator/about_us.html', context_dict)


def contact_us(request):
    context_dict = {}
    return render(request, 'gradinator/contact_us.html', context_dict)


def search(request):
    context_dict = {}
    return render(request, 'gradinator/search.html', context_dict)


def band_calculator(request):
    context_dict = {}
    return render(request, 'gradinator/band_calculator.html', context_dict)


def gpa_calculator(request):
    # view returns the object of the current user which contains a field called GPA
    # which  is not physically calculated here but by the model
    username = get_username(request)
    if username is not None:
        context_dict = {'user': User.objects.filter(GUID=username)}
        return render(request, 'gradinator/gpa_calculator.html', context_dict)


def get_username(request):
    # helper function that gets the username if the user is logged in
    if request.user.is_authenticated():
        username = request.user.username
        return username
    else:
        return None
