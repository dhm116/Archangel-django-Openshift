import autofixture
from autofixture import AutoFixture, generators
from models import *
from datetime import datetime

print 'Setting up CMS fixtures'

CourseFixture = AutoFixture(Course,
    field_values={
      'name': generators.LoremWordGenerator(count=2)
      ,'full_name': generators.LoremSentenceGenerator()
      ,'description': generators.LoremHTMLGenerator()
      ,'schedule_no': generators.PositiveIntegerGenerator(min_value=222222)
      ,'start_date': generators.DateGenerator(max_date=datetime.today())
      ,'end_date': generators.DateGenerator(min_date=datetime.today())
      ,'active': generators.StaticGenerator(True)
    }
  )


autofixture.register(Course, CourseFixture)

courses = autofixture.create(Course, 3)
print courses
