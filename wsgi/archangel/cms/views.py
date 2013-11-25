from django.contrib.auth.models import User, Group, Permission
from models import *
from rest_framework import viewsets, generics, authentication, permissions
from serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import *
from rest_framework.generics import *
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status, parsers, renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.renderers import (
    BaseRenderer,
    JSONRenderer,
    BrowsableAPIRenderer
)
from django.forms.models import model_to_dict
from django.db.models import Q, F
import datetime
# Create your views here.

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            user = model_to_dict(token.user)
            del user['password']
            return Response({'token': token.key, 'user':user})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
		"""
		API endpoint that allows users to be viewed or edited.
		"""
		# queryset = User.objects.all()
		model = User
		serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
		"""
		API endpoint that allows groups to be viewed or edited.
		"""
		model = Group
		# queryset = Group.objects.all()
		serializer_class = GroupSerializer

		def get_queryset(self):
				# Restrict permissions to those that you have
				return self.request.user.groups.all()

class PermissionViewSet(viewsets.ModelViewSet):
		"""
		API endpoint that allows permissions to be viewed or edited.
		"""
		model = Permission
		# queryset = Permission.objects.all()
		serializer_class = PermissionSerializer

		def get_queryset(self):
				# Restrict permissions to those that you have
				return self.request.user.user_permissions.all()

class CourseViewSet(viewsets.ModelViewSet):
		model = Course
		serializer_class = CourseSerializer

		def get_queryset(self):
				# Restrict courses to those that you belong to
				q = list(set(Course.objects.filter(sections__members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = Course.objects.filter(id__in=q)
				return q

class CourseSectionViewSet(viewsets.ModelViewSet):
		model = CourseSection
		serializer_class = CourseSectionSerializer

		def get_queryset(self):
				# Restrict course sections to those that you belong to
				q = list(set(CourseSection.objects.filter(members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = CourseSection.objects.filter(id__in=q)
				return q

class CourseRosterViewSet(viewsets.ModelViewSet):
		model = CourseRoster
		serializer_class = CourseRosterSerializer

		def get_queryset(self):
				# Restrict course roster to those in your same section
				q = list(set(CourseRoster.objects.filter(section__members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = CourseRoster.objects.filter(id__in=q)
				return q

class TeamViewSet(viewsets.ModelViewSet):
		model = Team
		serializer_class = TeamSerializer

		def get_queryset(self):
				q = list(set(Team.objects.filter(section__members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = Team.objects.filter(id__in=q)
				return q

class TeamMemberViewSet(viewsets.ModelViewSet):
		model = TeamMember
		serializer_class = TeamMemberSerializer

		def get_queryset(self):
				q = list(set(TeamMember.objects.filter(user__id=self.request.user.id).values_list('id', flat=True)))
				q = TeamMember.objects.filter(id__in=q)
				return q

class SyllabusViewSet(viewsets.ModelViewSet):
		model = Syllabus
		serializer_class = SyllabusSerializer

		def get_queryset(self):
				q = list(set(Syllabus.objects.filter(course__sections__members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = Syllabus.objects.filter(id__in=q)
				return q

class LessonViewSet(viewsets.ModelViewSet):
		model = Lesson
		serializer_class = LessonSerializer

		def get_queryset(self):
				q = list(set(Lesson.objects.filter(course__sections__members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = Lesson.objects.filter(id__in=q)
				return q

class AssignmentViewSet(viewsets.ModelViewSet):
		model = Assignment
		serializer_class = AssignmentSerializer

		def get_queryset(self):
				q = list(set(Assignment.objects.filter(lesson__course__sections__members__user__id=self.request.user.id).values_list('id', flat=True)))
				q = Assignment.objects.filter(id__in=q)
				return q

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
		model = AssignmentSubmission
		serializer_class = AssignmentSubmissionSerializer

		def get_queryset(self):
				q = list(set(AssignmentSubmission.objects.filter(Q(assignment__author__id=self.request.user.id) | Q(author__id=self.request.user.id)).values_list('id', flat=True)))
				q = AssignmentSubmission.objects.filter(id__in=q)
				return q

class GradedAssignmentSubmissionViewSet(viewsets.ModelViewSet):
		model = GradedAssignmentSubmission
		serializer_class = GradedAssignmentSubmissionSerializer

		def get_queryset(self):
				q = list(set(GradedAssignmentSubmission.objects.filter(Q(submission__assignment__author__id=self.request.user.id) | Q(author__id=self.request.user.id) | Q(submission__author__id=self.request.user.id)).values_list('id', flat=True)))
				q = GradedAssignmentSubmission.objects.filter(id__in=q)
				return q

class ForumViewSet(viewsets.ModelViewSet):
		model = Forum
		serializer_class = ForumSerializer

		def get_queryset(self):
				q = list(set(Forum.objects.filter(
					Q(course__sections__members__user__id=self.request.user.id)
					| Q(lesson__course__sections__members__user__id=self.request.user.id)
				).values_list('id', flat=True)))
				q = Forum.objects.filter(id__in=q)
				return q

class ForumPostViewSet(viewsets.ModelViewSet):
		model = ForumPost
		serializer_class = ForumPostSerializer

		def get_queryset(self):
				q = list(set(ForumPost.objects.filter(
					Q(author__id=self.request.user.id)
					| Q(response_to__author__id=self.request.user.id)
				).values_list('id', flat=True)))
				q = Message.objects.filter(id__in=q)
				return q

class DocumentViewSet(viewsets.ModelViewSet):
		model = Document
		serializer_class = DocumentSerializer

		def get_queryset(self):
				return Document.objects.filter(author__id=self.request.user.id)

class StudentsList(viewsets.ModelViewSet):
		# model = CmsUser
		serializer_class = UserSerializer
		student_group, created = Group.objects.get_or_create(name='student')
		queryset = User.objects.filter(courses__group_id=student_group.id)

class UpcomingAssignmentsList(ListAPIView):
		serializer_class = AssignmentSerializer
		model = Assignment
		# render_classes = (BrowsableAPIRenderer, JSONRenderer)

		def get_queryset(self):
				user = self.request.user
				# lessons = [course.lessons for course in courses]
				assignments = Assignment.objects.filter(lesson__course__sections__members__user__id=user.id,
						due_date__gte=datetime.date.today())
				return assignments

custom_obtain_auth_token = CustomObtainAuthToken.as_view()
upcoming_assignments = UpcomingAssignmentsList.as_view()
