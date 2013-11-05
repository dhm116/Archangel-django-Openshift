from django.contrib.auth.models import User, Group, Permission
from models import *
from rest_framework import serializers
from django.db.models.fields import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'email')

class CmsUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CmsUser
		fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'email', 'title', 'courses')

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name', 'permissions')
		depth = 1

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = ('id', 'name',)

class CourseSerializer(serializers.ModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()

	class Meta:
		model = Course
		fields = ('id', 'name', 'full_name', 'description', 'schedule_no', 'start_date', 'end_date' , 'sections', 'syllabus', 'lessons')
		# depth = 1

class CourseSectionSerializer(serializers.ModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()

	class Meta:
		model = CourseSection
		fields = ('id', 'section_no', 'course', 'members')

class CourseRosterSerializer(serializers.ModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()

	class Meta:
		model = CourseRoster
		fields = ('id', 'user', 'section', 'group')

class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id', 'author', 'name', 'description', 'content', 'file_path', 'creation_date')

class SyllabusSerializer(serializers.ModelSerializer):
	#author = serializers.RelatedField(view_name='instructor-detail')
	#course = serializers.RelatedField(view_name='course-detail')

	class Meta:
		model = Syllabus
		fields = ('id','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'course')
		# depth = 1

class LessonSerializer(serializers.ModelSerializer):
	#author = UserSerializer() #serializers.RelatedField(view_name='instructor-detail')
	#course = serializers.RelatedField() #serializers.RelatedField(view_name='course-detail')
	#assignments = serializers.RelatedField(view_name='assignment-detail', many=True)

	class Meta:
		model = Lesson
		fields = ('id','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'course', 'week_no')
		# depth = 1

class AssignmentSerializer(serializers.ModelSerializer):
	# author = serializers.RelatedField(view_name='instructor-detail')
	# lesson = serializers.RelatedField(view_name='lesson-detail')

	class Meta:
		model = Assignment
		fields = ('id','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'due_date', 'points', 'lesson')

class DocumentObjectRelatedField(serializers.RelatedField):
	def to_native(self, value):
		if isinstance(value, Syllabus):
			serializer = SyllabusSerializer(value)
		elif isinstance(value, Lesson):
			serializer = LessonSerializer(value)
		elif isinstance(value, Assignment):
			serializer = AssignmentSerializer(value)
		elif isinstance(value, Document):
			serializer = DocumentSerializer(value)
		else:
			raise Exception('Unexpected type of document object: ' + value.__class__.__name__)
		#serializer.data['__type__'] = value.__class__.__name__
		return serializer.data
