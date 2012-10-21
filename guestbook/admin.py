from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import Entry,Reply

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 1

class EntryAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
    list_display = ('user', 'submit_date', 'is_removed')
    list_filter = ['submit_date']
    date_hierarchy = 'submit_date'

admin.site.register(Entry, EntryAdmin)