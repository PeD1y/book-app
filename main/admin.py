# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Category,Book

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Book)
