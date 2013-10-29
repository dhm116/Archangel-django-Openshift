from django.contrib.auth.models import User, Group
from models import *
from rest_framework import viewsets, generics
from serializers import *

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
		"""
		API endpoint that allows users to be viewed or edited.
		"""
		# queryset = User.objects.all()
		model = User
		serializer_class = UserSerializer

class CmsUserViewSet(viewsets.ModelViewSet):
		"""
		API endpoint that allows users to be viewed or edited.
		"""
		# queryset = CmsUser.objects.all()
		model = CmsUser
		serializer_class = CmsUserSerializer

class GroupViewSet(viewsets.ModelViewSet):
		"""
		API endpoint that allows groups to be viewed or edited.
		"""
		model = Group
		# queryset = Group.objects.all()
		serializer_class = GroupSerializer

class CourseViewSet(viewsets.ModelViewSet):
		model = Course
		serializer_class = CourseSerializer

class CourseSectionViewSet(viewsets.ModelViewSet):
		model = CourseSection
		serializer_class = CourseSectionSerializer

class CourseRosterViewSet(viewsets.ModelViewSet):
		model = CourseRoster
		serializer_class = CourseRosterSerializer

class SyllabusViewSet(viewsets.ModelViewSet):
		model = Syllabus
		serializer_class = SyllabusSerializer

class LessonViewSet(viewsets.ModelViewSet):
		model = Lesson
		serializer_class = LessonSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
		model = Assignment
		serializer_class = AssignmentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
		model = Document
		serializer_class = DocumentSerializer

class StudentsList(viewsets.ModelViewSet):
		# model = CmsUser
		serializer_class = CmsUserSerializer
		student_group = Group.objects.get_or_create(name='student')
		queryset = CmsUser.objects.filter(courses__group_id=student_group.id)
