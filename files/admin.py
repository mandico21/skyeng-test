from django.contrib import admin

from files.models import FileUpload, FileReport


class FileReportInline(admin.TabularInline):
    model = FileReport
    extra = 0
    classes = ['collapse']
    verbose_name = 'Отче'
    verbose_name_plural = 'Отчеты'


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    inlines = [FileReportInline]


@admin.register(FileReport)
class FileReportAdmin(admin.ModelAdmin):
    ...
