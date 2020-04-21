from django.contrib import admin
from .models import TimeCard, VerificationCode

# Register your models here.
admin.site.register(TimeCard)
admin.site.register(VerificationCode)