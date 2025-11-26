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
STUDENT_SERVICE_URL = "http://127.0.0.1:9090/student/getOne"
def verify_student_exists(base_url, student_id):
    
    try:
        response = requests.get(f"{base_url}?id={student_id}", timeout=5)
        if response.status_code == 200 and response.json():
            return True
        elif response.status_code == 404:
            return False
        else:
            return False
    except requests.exceptions.RequestException:
        return None



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

@api_view(['POST'])
def enroll_student(request):
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')

    if not student_id or not course_id:
        return Response({"error": "student_id and course_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(course_id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    student_exists = verify_student_exists(STUDENT_SERVICE_URL, student_id)
    if student_exists is None:
        return Response({"error": "Student Service unreachable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if student_exists is False:
        return Response({"error": "Student not found in Student Service"}, status=status.HTTP_404_NOT_FOUND)

   
    if StudentCourse.objects.filter(student_id=student_id, course=course).exists():
        return Response({"message": "Student already enrolled in this course"}, status=status.HTTP_409_CONFLICT)


    enrollment = StudentCourse.objects.create(student_id=student_id, course=course)
    serializer = StudentCourseSerializer(enrollment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
