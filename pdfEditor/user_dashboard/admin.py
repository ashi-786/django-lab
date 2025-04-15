from django.contrib import admin
from .models import PdfFile, History

# Register your models here.
class PdfFileAdmin(admin.ModelAdmin):
    list_display = ("user", "html_file")

admin.site.register(PdfFile, PdfFileAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "file_fk", "html_file", "status", "updated_at")

admin.site.register(History, HistoryAdmin)