from django.urls import path
from . import views

urlpatterns = [
    path('courses', views.get_all_courses, name='get_all_courses'),
    path('courses/<int:course_id>', views.get_course, name='get_course'),
    path('courses/add', views.add_course, name='add_course'),
    path('courses/update/<int:course_id>', views.update_course, name='update_course'),
    path('courses/delete/<int:course_id>', views.delete_course, name='delete_course'),
    path('courses/search', views.search_courses, name='search_courses'),
    
]
