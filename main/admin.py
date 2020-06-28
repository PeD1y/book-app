# Register your models here.
from django.contrib import admin
from .models import User,Category,Book
from django.contrib.auth.admin import UserAdmin



admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Book)
