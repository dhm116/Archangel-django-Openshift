import unittest
from django.utils import unittest
from django.test import TestCase
from selenium import webdriver
from django.utils import timezone
from cms.models import Course


class CourseTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_course_via_admin_site(self):
         # User opens the web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # user sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # User types in the username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('abdulatif')
        password_field.send_keys('a210110')
        #password_field.send_keys(Keys.RETURN)

        # the username and password are accepted, and user is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # user now sees a several of hyperlink that says "course"
        course_links = self.browser.find_elements_by_link_text('Course')
        self.assertEquals(len(Course_links), 2)

        # TODO: the user uses the admin site to create a new course
        self.fail('todo: finish tests')


class AdminCustomisationTest(unittest.TestCase):
    
    def setUp(self):
        username = 'abdulatif'
        pwd = 'a210110'

        self.u = Client.objects.create_user(username, '', pwd)
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.save()

        self.assertTrue(self.client.login(username=username, password=pwd),
            "Logging in user %s, pwd %s failed." % (username, pwd))

        Client.objects.all().delete()

    def tearDown(self):
        self.client.logout()
        self.u.delete()

    def test_add_course_ok(self):
        self.assertEquals(Course.objects.count(), 0)

        post_data = { 'title': u'Test OK',
                      'open_date': datetime.now(),
                    }

        response = self.client.post(reverse('admin:course_add'), post_data)

        self.assertRedirects(response, reverse('admin:course_changelist'))
        self.assertEquals(Survey.objects.count(), 1)        


class CourseModelTest(TestCase):
    def test_creating_a_new_course_and_saving_it_to_the_database(self):
        # start by creating a new course object with its "add course" set
        course = Course()
        course.create = "SWENG505"
        course.create_date = timezone.now()

        # check we can save it to the database
        course.save()

        # now check we can find it in the database again
        all_courses_in_database = Course.objects.all()
        self.assertEquals(len(all_Courses_in_database), 1)
        only_Courses_in_database = all_Courses_in_database[0]
        self.assertEquals(only_Courses_in_database, Course)

        # and check that it's saved its two attributes: create and Create_date
        self.assertEquals(only_Course_in_database.create, "SWENG505")
        self.assertEquals(only_Course_in_database.Create_date, Course.create_date)
