from django.contrib import admin
from ddtcms.member.models import EmailValidation, Avatar
from ddtcms.member.models import Profile,Resume,Favourite

class EmailValidationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('user__username', 'user__first_name')

admin.site.register(Avatar)
admin.site.register(EmailValidation, EmailValidationAdmin)
admin.site.register(Profile)
admin.site.register(Resume)
admin.site.register(Favourite)