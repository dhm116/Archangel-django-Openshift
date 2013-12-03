from django.contrib.auth.models import User, Group, Permission
from models import *
from rest_framework import serializers
from django.db.models.fields import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'email', 'courses', 'profile')

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name', 'permissions')
		depth = 1

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = ('id', 'name',)

class CourseRosterSerializer(serializers.ModelSerializer):
	# documents = DocumentObjectRelatedField(many=True)#, context={'request':request})
	# syllabus = SyllabusSerializer()
	course = serializers.Field('course.id')
	group = serializers.RelatedField()

	class Meta:
		model = CourseRoster
		fields = ('id', 'user', 'section', 'group', 'course')

class CourseSectionSerializer(serializers.ModelSerializer):
	# members = CourseRosterSerializer(required=False, many=True)

	class Meta:
		model = CourseSection
		fields = ('id', 'section_no', 'course', 'members', 'teams')

class CourseSerializer(serializers.ModelSerializer):
	# sections = CourseSectionSerializer(required=False, many=True)

	class Meta:
		model = Course
		fields = ('id', 'name', 'full_name', 'description', 'schedule_no', 'start_date', 'end_date' , 'sections', 'syllabus', 'lessons', 'forums')
		# depth = 1

class TeamSerializer(serializers.ModelSerializer):
	course = serializers.Field('course.id')

	class Meta:
		model = Team
		fields = ('id', 'members', 'section', 'team_no', 'name', 'course')

class TeamMemberSerializer(serializers.ModelSerializer):
	section = serializers.Field('team.section.id')
	course = serializers.Field('team.course.id')

	class Meta:
		model = TeamMember
		fields = ('id', 'team', 'user', 'section', 'course')

class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = ('id', 'author', 'name', 'description', 'content', 'file_path', 'creation_date')

class SyllabusSerializer(serializers.ModelSerializer):

	class Meta:
		model = Syllabus
		fields = ('id','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'course')
		# depth = 1

class LessonSerializer(serializers.ModelSerializer):

	class Meta:
		model = Lesson
		fields = ('id','author', 'name', 'description', 'content', 'file_path', 'creation_date', 'course', 'week_no', 'assignments', 'forums')
		# depth = 1

class AssignmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Assignment
		fields = ('id','author', 'name', 'description', 'content', 'creation_date', 'file_path', 'due_date', 'points', 'weight', 'lesson','submissions')

class AssignmentSubmissionSerializer(serializers.ModelSerializer):

	class Meta:
		model = AssignmentSubmission
		fields = ('id','author', 'team', 'name', 'description', 'content', 'file_path', 'creation_date', 'submitted_date', 'assignment', 'grade')

class GradedAssignmentSubmissionSerializer(serializers.ModelSerializer):
	assignment = serializers.Field('assignment.id')

	class Meta:
		model = GradedAssignmentSubmission
		fields = ('id','author', 'name', 'description', 'content', 'creation_date', 'file_path', 'submission', 'score', 'assignment')

class ForumSerializer(serializers.ModelSerializer):
	class Meta:
		model = Forum
		fields = ('id', 'course', 'lesson', 'name', 'description')

class ForumPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = ForumPost
		fields = ('id', 'author', 'response_to', 'name', 'description', 'content', 'creation_date', 'replies')
		# depth = 1

class ForumPostAttachmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ForumPostAttachment
		fields = ('id', 'author', 'post', 'name', 'description', 'content', 'creation_date')

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
