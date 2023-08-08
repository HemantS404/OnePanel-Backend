from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')

# Register your models here.
admin.site.register(User, UserAdmin)