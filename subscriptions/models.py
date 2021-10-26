from django.db import models
from users.models import User
from apps.models import App
from datetime import datetime

# Create your models here.
class Plan(models.Model):

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    plan = models.ForeignKey(Plan, on_delete=None)
    app = models.ForeignKey(App, on_delete=None)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'app'],
                                    name='UserAppPlan'),
        ]
    def __str__(self):
        return self.user.username
