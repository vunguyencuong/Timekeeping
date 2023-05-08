from email.policy import default
from django.db import models
import datetime


# Create your models here.
GENDER_CHOICES = ((0,"Unkown"),(1,"Female"),(2,"Male"))
EDUCATION_LEVEL = ((0,"Unkown"),(1,"High School"), (2,"Bachelor"))

class Employee(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    birthDay = models.DateField(default='2000-01-01')
    homeTown = models.CharField(max_length=100, default="Unkown")
    phone = models.CharField(max_length=20, default="Unkown")
    gender = models.IntegerField(default=0, choices=GENDER_CHOICES)
    educationLevel = models.IntegerField(default=0, choices=EDUCATION_LEVEL)

    avatar = models.ImageField(default = 'unkown.jpg')
    embedding = models.BinaryField()

    def __str__(self):
        return f'{self.id} - {self.name}'

class Checkin(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.employee.id} - {self.employee.name} - {self.date}'

class Query(models.Model):
    avatar = models.ImageField(default = 'unkown.jpg')
    embedding = models.BinaryField()
