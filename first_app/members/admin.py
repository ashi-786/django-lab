from django.contrib import admin
from .models import Member

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("fname", "lname", "phone", "joined_date",)
    prepopulated_fields = {"slug" : ("fname", "lname")}

admin.site.register(Member, MemberAdmin)