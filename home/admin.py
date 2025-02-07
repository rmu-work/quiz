from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = "Quiz Arena"
admin.site.site_title = "Quiz Arena"

admin.site.unregister(Group)
