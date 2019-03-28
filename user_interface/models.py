from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
# All objects in the project that are
# django Model objects

# class Person(models.Model):
# 	name = models.CharField(max_length=200)
# 	phone_number = models.PositiveIntegerField(
# 			default = 1000000000,
# 			validators=[MaxValueValidator(9999999999),
# 			MinValueValidator(1000000000)]
# 		)
# 	birthday = models.DateField(
# 			validators=[
# 			MaxValueValidator(datetime.date.today())]
# 		)
# 	calendar_data = models.TextField()
#
# 	#def __str__(self):
# 	#	return self.person_name
