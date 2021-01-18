from django.contrib import admin
from .models import Order

admin.site.register(Order)

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()