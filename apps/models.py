from django.db import models
from django.core.validators import URLValidator
from users.models import User
from datetime import datetime
from enum import Enum

# Create your models here.
class App(models.Model):

    class appType(Enum):
        ty1  = 'Web'
        ty2  = 'Mobile'

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    class appFrameWork(Enum):
        fw1  = 'Django'
        fw2  = 'React Native'

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    name    =   models.CharField(max_length=50, null=False, unique=True) # validators=[minLengthValidator(1)])
    description = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=appType.choices())
    framework = models.CharField(max_length=50, choices=appFrameWork.choices())
    domain_name = models.CharField(max_length=50, null=True)
    screenshot = models.CharField(max_length=100, validators=[URLValidator()], null=True)
    user = models.ForeignKey(User, on_delete=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name