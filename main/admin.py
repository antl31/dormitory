# Register your models here.
from django.contrib import admin

from .models import Hostel, Room,  CustomUser


admin.site.register(Hostel)
admin.site.site_header = "Dormitory Administration"


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('room', 'hostel', 'group')

    list_display = ['first_name', 'last_name', 'email', 'hostel', 'room', 'is_active']
    fields = ['first_name', 'last_name', 'email', 'course', 'group', 'hostel', 'room', "is_active"]
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    change_list_template = "admin/main_list.html"


class RoomAdmin(admin.ModelAdmin):
    list_filter = ('hostel', 'floor', 'max_quantity', 'now_quantity')
    list_display = ['hostel', 'floor', 'number', 'max_quantity', 'now_quantity']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Room, RoomAdmin)
