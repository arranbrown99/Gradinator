import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradinator_project.settings')
import django

django.setup()
from gradinator.models import Course
from gradinator.models import Coursework


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models

    wad_coursework = [
        {"name": "WAD Rango Application",
         "course": "wad",
         "weight": 0.1},
        {"name": "WAD Quiz",
         "course": "wad",
         "weight": 0.1},
        {"name": "WAD Group Project Application",
         "course": "wad",
         "weight": 0.25},
        {"name": "Wad Group Project Design Specification",
         "course": "wad",
         "weight": 0.1},
        {"name": "WAD Group Project Presentation",
         "course": "wad",
         "weight": 0.05},
        {"name": "WAD Exam",
         "course": "wad",
         "weight": 0.4}
    ]
    oose_coursework = [
        {"name": "OOSE Workshop 1",
         "course": "oose",
         "weight": 0.05},
        {"name": "OOSE Workshop 2",
         "course": "oose",
         "weight": 0.05},
        {"name": "OOSE Workshop 3",
         "course": "oose",
         "weight": 0.1},
        {"name": "OOSE Exam",
         "course": "oose",
         "weight": 0.8},
    ]
    ads_coursework = [
        {"name": "ADS assessed exercise 1",
         "course": "ads",
         "weight": 0.1},
        {"name": "ADS assessed exercise 2",
         "course": "ads",
         "weight": 0.1},
        {"name": "ADS exam",
         "course": "ads",
         "weight": 0.8},
    ]
    nose_coursework = [
        {"name": "NOSE Assessed Exercise 1",
         "course": "nose",
         "weight": 0.1},
        {"name": "NOSE Assessed Exercise 2",
         "course": "nose",
         "weight": 0.1},
        {"name": "NOSE Exam",
         "course": "nose",
         "weight": 0.8},
    ]
    af_coursework = [
        {"name": "AF2 Assessed Exercise 1",
         "course": "af",
         "weight": 0.1},
        {"name": "AF2 Assessed Exercise 2",
         "course": "af",
         "weight": 0.1},
        {"name": "AF2 Exam",
         "course": "af",
         "weight": 0.8},
    ]
    jp2_coursework = [
        {"name": "JP2 Lab Exam",
         "course": "jp2",
         "weight": 0.2},
        {"name": "JP2 Exam",
         "course": "jp2",
         "weight": 0.6},
        {"name": "JP2 Lab 1",
         "course": "jp2",
         "weight": 0.04},
        {"name": "JP2 Lab 2",
         "course": "jp2",
         "weight": 0.04},
        {"name": "JP2 Lab 3",
         "course": "jp2",
         "weight": 0.04},
        {"name": "JP2 Lab 4",
         "course": "jp2",
         "weight": 0.04},
        {"name": "JP2 Lab 5",
         "course": "jp2",
         "weight": 0.04},
    ]

    courses = {"WAD": {"name": "Web App Development",
                       "id": "COMPSCI 2021",
                       "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2021",
                       "taught_by": "David Manlove",
                       "description": "The aim of this course is to provide students with a comprehensive overview of web application development. It will provide students with the skills to design and develop distributed web applications in a disciplined manner, using a range of tools and technologies. It will also strengthen their understanding of the context and rationale of distributed systems. ",
                       "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt. Strong python skills are a requirement for this course.",
                       "credits": 10,
                       "year": 2,
                       "school": "School of Computing Science",
                       "coursework": wad_coursework,
                       },

               "OOSE": {"name": "Object Orientated Software Engineering",
                        "id": "COMPSCI 2008",
                        "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2008",
                        "taught_by": "Inah Omoronyia",
                        "description": "This course introduces the basic concepts of software engineering. Students will learn methods for the design, implementation, testing and documentation of larger object-oriented programs, and will also develop program comprehension and design skills by studying and extending existing programs.",
                        "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt",
                        "credits": 10,
                        "year": 2,
                        "school": "School of Computing Science",
                        "coursework": oose_coursework},

               "ADS": {"name": "Algorithms and Data Structures",
                       "id": "COMPSCI 2007",
                       "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2007",
                       "taught_by": "Michele Sevegnani",
                       "description": "To familiarise students with fundamental data types and data structures used in programming, with the design and analysis of algorithms for the manipulation of such structures, and to provide practice in the implementation and use of these structures and algorithms in a Java context.",
                       "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt.",
                       "credits": 10,
                       "year": 2,
                       "school": "School of Computing Science",
                       "coursework": ads_coursework,

                       },

               "NOSE": {"name": "Networks and operating system essentials 2",
                        "id": "COMPSCI 2024",
                        "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2024",
                        "taught_by": "Nikos Ntarmos and Maria Evangelopoulou",
                        "description": "The course will introduce students to essential topics in computer networks and operating systems. It has a focus on the underlying concepts, design, and operation of the Internet, and on the role, basic features, and principles of computer operating systems.",
                        "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt.",
                        "credits": 10,
                        "year": 2,
                        "school": "School of Computing Science",
                        "coursework": nose_coursework,

                        },

               "AF2": {"name": "Algorithmic Foundations 2",
                       "id": "COMPSCI 2003",
                       "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2003",
                       "taught_by": "Gethin Norman",
                       "description": "To introduce the foundational mathematics needed for Computing Science; To make students proficient in their use; To show how they can be applied to advantage in understanding computational phenomena.",
                       "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt.",
                       "credits": 10,
                       "year": 2,
                       "school": "School of Computing Science",
                       "coursework": af_coursework,

                       },
               "JP2": {"name": "Java Programming 2",
                       "id": "COMPSCI 2001",
                       "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2001",
                       "taught_by": "Mary Ellen Foster",
                       "description": "This course extends students' experience in programming using a strongly typed language (Java) and strengthens their problem solving skills. Students will learn the ideas that underpin object-oriented programming and will apply those concepts in developing small and medium sized software systems. Students will also learn to select and re-use existing software components and libraries, and will gain experience in concurrent programming and elementary graphical user-interface (GUI) development.",
                       "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt.",
                       "credits": 10,
                       "year": 2,
                       "school": "School of Computing Science",
                       "coursework": jp2_coursework,
                       }}

    # If you want to add more courses or coursework
    # add them to the dictionaries above

    # The code below goes through the course dictionary, then adds each course,
    # and then adds all the associated pages for that category.
    for course, course_data in courses.items():
        c = add_course(course_data["name"], course_data["id"], course_data["url"], course_data["taught_by"],
                       course_data["description"],
                       course_data["requirements_of_entry"], course_data["credits"], course_data["year"],
                       course_data["school"])
        for cw in course_data["coursework"]:
            add_coursework(c, cw["name"], cw["weight"])

    # Print out the courses we have added.
    for c in Course.objects.all():
        for cw in Coursework.objects.filter(course=c):
            print("- {0} - {1}".format(str(c), str(cw)))


def add_coursework(course, name, weight):
    cw = Coursework.objects.get_or_create(course=course, name=name)[0]
    cw.course = course
    cw.name = name
    cw.weight = weight * 100
    cw.save()
    return cw


# for testing mostly
def add_course_and_coursework(course, coursework, name):
    c = add_course(course[name]["name"], course[name]["id"], course[name]["url"], course[name]["taught_by"],
                   course[name]["description"],
                   course[name]["requirements_of_entry"], course[name]["credits"], course[name]["year"],
                   course[name]["school"])

    if coursework == course[name]["coursework"]:
        for this in coursework:
            add_coursework(c, this["name"], this["weight"])

    return c


def add_course(name, id, url, taught_by, description,
               requirements_of_entry, course_credits, year,
               school):
    c = Course.objects.get_or_create(id=id)[0]
    c.name = name
    c.id = id
    c.url = url
    c.taught_by = taught_by
    c.description = description
    c.requirements_of_entry = requirements_of_entry
    c.credits = course_credits
    c.year = year
    c.school = school
    c.save()
    return c


if __name__ == '__main__':
    print("Starting Gradinator population script...")
    populate()
