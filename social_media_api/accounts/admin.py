from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	fieldsets = DjangoUserAdmin.fieldsets + (
		('Profile', {'fields': ('bio', 'profile_picture', 'followers')}),
	)
	list_display = ('username', 'email', 'first_name', 'last_name', 'followers_count')

	def followers_count(self, obj):
		return obj.followers.count()
	followers_count.short_description = 'Followers'
