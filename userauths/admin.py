from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email')
    list_display = ['username', 'full_name', 'email', 'phone', 'gender', 'is_staff', 'is_superuser']
    
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email')
    list_display = ['user', 'full_name']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
