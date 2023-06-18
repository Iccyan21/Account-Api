from django.contrib import admin
from .models import AccessToken, User


admin.site.register(AccessToken)
admin.site.register(User)
# Register your models here.
