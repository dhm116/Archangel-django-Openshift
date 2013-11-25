from django.conf.urls import patterns, include, url
from rest_framework import routers
from cms.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import autofixture

admin.autodiscover()
autofixture.autodiscover()
print autofixture.REGISTRY

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'coursesections', CourseSectionViewSet)
router.register(r'courserosters', CourseRosterViewSet)
router.register(r'syllabuses', SyllabusViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'assignmentsubmissions', AssignmentSubmissionViewSet)
router.register(r'gradedassignmentsubmissions', GradedAssignmentSubmissionViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'students', StudentsList)
router.register(r'teams', TeamViewSet)
router.register(r'teammembers', TeamMemberViewSet)
router.register(r'forums', ForumViewSet)
router.register(r'forumposts', ForumPostViewSet)
# router.register(r'upcoming-assignments', UpcomingAssignmentsList)
# router.register(r'auth-token/$', 'rest_framework.authtoken.views.obtain_auth_token')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'archangel.views.home', name='home'),
    # url(r'^archangel/', include('archangel.foo.urls')),
    url(r'^', include(router.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^doc/', include('rest_framework_swagger.urls')),
    url(r'^api-token-auth/', 'cms.views.custom_obtain_auth_token'),
    url(r'^upcoming-assignments/', 'cms.views.upcoming_assignments'),
)
