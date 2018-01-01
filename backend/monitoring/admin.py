"""Settings for the admin page.
"""
from django.contrib import admin
from monitoring.models import Feedback, Metric


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'time', 'value')
    list_filter = ('name', 'group')
    search_fields = ('name', 'group')
    date_hierarchy = 'time'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    date_hierarchy = 'inserted'
    list_filter = ('inserted', 'url')
    search_fields = ['comment']
