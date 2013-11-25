from django.db import models
from django.contrib.auth.models import User, Group
from model_utils.managers import InheritanceManager
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.get_or_create(user=instance)
		UserProfile.objects.get_or_create(user=instance)

class UserProfile(models.Model):
	bio = models.TextField(blank=True)
	picture = models.URLField(blank=True)
	title = models.CharField(max_length=200, blank=True)
	user = models.OneToOneField(User, related_name='profile')

class Role(Group):
	pass

class Course(models.Model):
	name = models.CharField(max_length=400, null=False)
	full_name = models.TextField()
	description = models.TextField(blank=True)
	schedule_no = models.CharField(max_length=7, null=False, unique=True)
	start_date = models.DateField(null=False)
	end_date = models.DateField(null=False)
	active = models.BooleanField(null=False, default=False)

	def __unicode__(self):
		return u'#%s %s : %s'%(self.schedule_no, self.name, self.full_name)

class CourseSection(models.Model):
	section_no = models.CharField(max_length=7, null=False, verbose_name='Course Section')
	course = models.ForeignKey(Course, related_name='sections')

	def __unicode__(self):
		return u'%s section %s'%(self.course.name, self.section_no)

	class Meta:
		unique_together = (('section_no', 'course'),)
		# order_with_respect_to = 'course'
		ordering = ['section_no']

class CourseRoster(models.Model):
	user = models.ForeignKey(User, related_name='courses')
	section = models.ForeignKey(CourseSection, related_name='members')
	# role = models.ForeignKey(Role)
	group = models.ForeignKey(Group)

	class Meta:
		unique_together = (('user', 'section'),)

	def _get_course(self):
		return self.section.course

	course = property(_get_course)

	def __unicode__(self):
		return u'%s -> %s -> %s'%(self.user, self.section, self.group)

class Team(models.Model):
	section = models.ForeignKey(CourseSection, related_name='teams')
	team_no = models.PositiveIntegerField()
	name = models.CharField(max_length=200, null=True, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	def _get_course(self):
		return self.section.course

	course = property(_get_course)

	class Meta:
		unique_together = (('section', 'team_no'),)
		ordering = ['team_no']

class TeamMember(models.Model):
	user = models.ForeignKey(User, related_name='teams')
	team = models.ForeignKey(Team, related_name='members')

	class Meta:
		unique_together = (('user', 'team'),)
		ordering = ['team']

class Document(models.Model):
	author = models.ForeignKey(User)
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True)
	content = models.TextField(blank=True, null=True)
	file_path = models.CharField(max_length=400, blank=True, null=True)
	creation_date = models.DateTimeField(auto_now_add=True)
	objects = InheritanceManager()
	# course = models.ForeignKey(Course, related_name='documents')

class Syllabus(Document):
	course = models.OneToOneField(Course, null=False, related_name='syllabus')

	class Meta:
		verbose_name = 'Syllabus'
		verbose_name_plural = 'Syllabuses'

	def __unicode__(self):
		return u'%s -> %s'%(self.course, self.name)

class Lesson(Document):
	course = models.ForeignKey(Course, related_name='lessons')
	week_no = models.PositiveIntegerField()

	class Meta:
		verbose_name = 'Lesson'
		verbose_name_plural = 'Lessons'
		# order_with_respect_to = 'course'
		ordering = ['week_no']

	def __unicode__(self):
		return u'%s -> Week %s'%(self.course, self.week_no)

class Assignment(Document):
	due_date = models.DateTimeField()
	points = models.DecimalField(max_digits=5, decimal_places=0)
	weight = models.DecimalField(max_digits=4, decimal_places=3)
	lesson = models.ForeignKey(Lesson, related_name='assignments')

	class Meta:
		verbose_name = 'Assignment'
		verbose_name_plural = 'Assignments'
		ordering = ['due_date']

	def __unicode__(self):
		return u'%s -> %s'%(self.lesson, self.name)

class AssignmentSubmission(Document):
	assignment = models.ForeignKey(Assignment, related_name='submissions')
	team = models.ForeignKey(Team, related_name='submissions', blank=True, null=True)
	submitted_date = models.DateTimeField(auto_now_add=True)
	# score = models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		# order_with_respect_to = 'assignment'
		ordering = ['-submitted_date']

	def _get_lesson(self):
		return self.assignment.lesson

	lesson = property(_get_lesson)

class GradedAssignmentSubmission(Document):
	# assignment = models.ForeignKey(Assignment, related_name='grades')
	submission = models.OneToOneField(AssignmentSubmission, null=False, related_name='grade')
	score = models.DecimalField(max_digits=5, decimal_places=2)

	def _get_assignment(self):
		return self.submission.assignment

	assignment = property(_get_assignment)

	def _get_submission_author(self):
		return self.submission.author

	submission_author = property(_get_submission_author)

	class Meta:
		verbose_name = 'Graded Assignment'
		verbose_name_plural = 'Graded Assignments'

class Forum(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True)
	course = models.ForeignKey(Course, related_name='forums', blank=True, null=True)
	lesson = models.ForeignKey(Lesson, related_name='forums', blank=True, null=True)

class ForumPost(Document):
	response_to = models.ForeignKey('self', related_name='replies', null=True, blank=True)
	forum = models.ForeignKey(Forum, related_name='posts')

class ForumPostAttachment(Document):
	post = models.ForeignKey('ForumPost', related_name='attachments')

