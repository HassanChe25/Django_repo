from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Course , StudentCourse
from .serializers import CourseSerializer , StudentCourseSerializer
from django.db.models import Q
import requests



@api_view(['POST'])
def add_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "New course is added"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    serializer = CourseSerializer(course)
    return Response(serializer.data)



@api_view(['PUT'])
def update_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Course updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return Response({"message": "Course deleted successfully"})


@api_view(['GET'])
def search_courses(request):
    keyword = request.query_params.get('keyword', '')
    if not keyword:
        return Response({"error": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST)

    courses = Course.objects.filter(
        Q(name__icontains=keyword) |
        Q(instructor__icontains=keyword) |
        Q(category__icontains=keyword)
    )
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

