from django.shortcuts import render


# Create your views here.
def home(request):
    context_dict = {}
    return render(request, 'gradinator/home.html', context_dict)

def signup(request):
    context_dict = {}
    return render(request, 'gradinator/account/signup.html', context_dict)

def login(request):
    context_dict = {}
    return render(request, 'gradinator/account/login.html', context_dict)

def account(request):
    context_dict = {}
    return render(request, 'gradinator/account.html', context_dict)

def mycourses(request):
    context_dict = {}
    return render(request, 'gradinator/mycourses.html', context_dict)

def show_course(request,course_name_slug):
    context_dict = {}
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
    context_dict = {}
    return render(request, 'gradinator/gpa_calculator.html', context_dict)
