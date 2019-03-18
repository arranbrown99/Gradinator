from django.contrib import admin
from gradinator.models import UserGrade
from gradinator.models import UserProfile
from gradinator.models import Course
from gradinator.models import Coursework
from gradinator.models import UserCourseworkGrade


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')


class CourseworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')


class UserGradeAdmin(admin.ModelAdmin):
    list_display = ('grade_for', 'sat_by', 'grade')


class UserCourseworkGradeAdmin(admin.ModelAdmin):
    list_display = ('grade_for', 'sat_by', 'grade')


admin.site.register(Course, CourseAdmin)
admin.site.register(Coursework, CourseworkAdmin)

admin.site.register(UserProfile)
admin.site.register(UserGrade, UserGradeAdmin)
admin.site.register(UserCourseworkGrade,UserCourseworkGradeAdmin)
