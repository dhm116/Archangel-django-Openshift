from django.contrib.auth.models import User, Group, Permission
from models import *
from rest_framework import serializers
from django.db.models.fields import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'email', 'groups',)

class CmsUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = CmsUser
		fields = ('url', 'id', 'username', 'email', 'title', 'groups', 'courses')

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name', 'permissions')
		depth = 1

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = ('id', 'name',)

class CourseSerializer(serializers.HyperlinkedModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()

	class Meta:
		model = Course
		fields = ('url', 'id', 'name', 'full_name', 'description', 'schedule_no', 'start_date', 'end_date' , 'sections', 'syllabus', 'lessons')
		# depth = 1

class CourseSectionSerializer(serializers.HyperlinkedModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()

	class Meta:
		model = CourseSection
		fields = ('url', 'id', 'section_no', 'course', 'members')

class CourseRosterSerializer(serializers.HyperlinkedModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()

	class Meta:
		model = CourseRoster
		fields = ('url', 'id', 'user', 'section', 'group')

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Document
		fields = ('url','author', 'name', 'description', 'content', 'file_path', 'creation_date')

class SyllabusSerializer(serializers.HyperlinkedModelSerializer):
	#author = serializers.HyperlinkedRelatedField(view_name='instructor-detail')
	#course = serializers.HyperlinkedRelatedField(view_name='course-detail')

	class Meta:
		model = Syllabus
		fields = ('url','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'course')
		# depth = 1

class LessonSerializer(serializers.HyperlinkedModelSerializer):
	#author = UserSerializer() #serializers.HyperlinkedRelatedField(view_name='instructor-detail')
	#course = serializers.RelatedField() #serializers.HyperlinkedRelatedField(view_name='course-detail')
	#assignments = serializers.HyperlinkedRelatedField(view_name='assignment-detail', many=True)

	class Meta:
		model = Lesson
		fields = ('url','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'course', 'week_no')
		# depth = 1

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
	# author = serializers.HyperlinkedRelatedField(view_name='instructor-detail')
	# lesson = serializers.HyperlinkedRelatedField(view_name='lesson-detail')

	class Meta:
		model = Assignment
		fields = ('url','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'due_date', 'points', 'lesson')

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
