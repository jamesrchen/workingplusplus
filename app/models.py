from django.conf import settings
from django.db import models


# Create your models here.
from django.utils import timezone


class TimeCard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    completed = models.BooleanField(name="completed", default=False)
    timeIn = models.DateTimeField(name="timeIn")
    timeOut = models.DateTimeField(name="timeOut", null=True)

    def __str__(self):
        if self.completed:
            return "Completed TimeCard"
        else:
            return "Uncompleted TimeCard"


class VerificationCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    code = models.TextField()
    expiryDate = models.DateTimeField(default=timezone.now()+timezone.timedelta(minutes=5))

    def __str__(self):
        return self.code
