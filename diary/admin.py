from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Task, Profile

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Profile)