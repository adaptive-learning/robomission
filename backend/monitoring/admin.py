"""Settings for the admin page.
"""
from django.contrib import admin
from monitoring.models import Metric


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'time', 'value')
    list_filter = ('name', 'group')
    search_fields = ('name', 'group')
    date_hierarchy = 'time'
