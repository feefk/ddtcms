# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: 
# Creation Date: 
# Last Modified: 
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#
# ------------------------------------------------------------

# django.
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
from ddtcms.blog.models import Blog
from ddtcms.blog.models import Category
from ddtcms.blog.forms  import CreateBlogForm,MyBlogAdminForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------





#class BlogBlogAdminForm(forms.ModelForm):
#    BLOOD_CHOICES = (
#        (u'A型', u'A型'),
#        (u'B型', u'B型'),
#        (u'O型', u'O型'),
#        (u'AB型',u'AB型'),
#    )
#    class Meta:
#        model = Blog
#
#    #queries = {'user':'admin'}
#    #category = forms.ChoiceField(choices=Category.objects.all().filter(**queries))
#    #category = forms.ChoiceField(choices=Category.objects.all())
#    #category = forms.ChoiceField(choices=[(c.id,c.name) for c in Category.objects.all()])
#    #category = forms.ChoiceField(choices=Category.objects.for_model(Blog))
#    #category = forms.ChoiceField(choices=BLOOD_CHOICES)
#    #category=forms.ModelChoiceField(queryset=Category.objects.all().filter(**queries))
#    #category=forms.ModelChoiceField(queryset=Category.objects.all())
#    #category=forms.ModelChoiceField(queryset=Category.objects.all().filter(**queries))
#    #def clean_title(self):
#    #    # do something that validates your data
#    #    return self.cleaned_data["title"]



class BlogAdmin(admin.ModelAdmin):
    #form = BlogBlogAdminForm
    form = MyBlogAdminForm
    
    #http://code.djangoproject.com/wiki/NewformsHOWTO
    #Lllama's handy how-do-I guide to newforms admin.
    #Q: How do I filter the ChoiceField? based upon attributes of the current ModelAdmin? instance? 
    #Ticket #3987 http://code.djangoproject.com/ticket/3987
    #
#    def __call__(self, request, url):
#        #Add in the request object, so that it may be referenced
#        #later in the formfield_for_dbfield function.
#        self.request = request
#        return super(BlogAdmin, self).__call__(request, url)
#    
#    def formfield_for_dbfield(self, db_field, **kwargs):
#        
#        field = super(BlogAdmin, self).formfield_for_dbfield(db_field, **kwargs) # Get the default field
#        request = kwargs.pop("request", None)
#        if db_field.name == 'category': 
#            #Add the null object
#            my_choices = [('', '---------')]
#            #Grab the current site id from the URL.
#            if request:
#                my_choices.extend(Category.objects.filter(user=request.user).values_list('id','name'))
#            else:
#                my_choices.extend(Category.objects.all().values_list('id','name'))    
#            #print my_choices
#            field.choices = my_choices
#        return field
#
#    
#    def queryset(self, request):
#        if request.user.is_superuser:
#            return super(BlogAdmin, self).queryset(request)
#        else:
#            queries = {'user':request.user}
#            return super(BlogAdmin, self).queryset(request).filter(**queries)
            

            #app, model = "blog.Blog".split('.')
            #content_type=ContentType.objects.get(app_label=app, model=model)
            #queries = {'category.content_type':content_type}

               
    #def save_model(self, request, obj, form, change):
    #    obj.user = request.user
    #    return super(BlogAdmin, self).save_model(request, obj, form, change)
    
    #def add_view(self, request, form_url='', extra_context=None):
    #    ex_context={'category':Category.objects.for_model(Blog)}
    #    return super(BlogAdmin, self).add_view(request, form_url='', extra_context=ex_context)

    #def add_view(self, request, form_url='', extra_context=None):
    #    ex_context={'category':Category.objects.for_model(Blog)}
    #    return super(BlogAdmin, self).add_view(request, form_url='', extra_context=ex_context)
    
    #
    #CODE FROM :
    #URL:  http://code.djangoproject.com/wiki/CookBookNewformsAdminAndUser
    #TITLE:How to set the current user on the model instance in the admin (newforms-admin) 
    #
    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change): 
        def set_user(instance):
            instance.user = request.user
            instance.save()

        if formset.model == Comment:
            instances = formset.save(commit=False)
            map(set_user, instances)
            formset.save_m2m()
            return instances
        else:
            return formset.save()

    
    fieldsets = [
        ('标题',             {'fields': ['title']}),
        ('简短标记',         {'fields': ['slug']}),
        #('所属用户',         {'fields': ['user']}),
        ('所属分类',         {'fields': ['category']}),
        ('Date information', {'fields': ['pub_date']}),
        ('内容',             {'fields': ['content']}),
        ('摘要',             {'fields': ['summary']}),
        ('Tags',             {'fields': ['tags']}), 
        #('Views',            {'fields': ['views']}),
        #('Comments',         {'fields': ['comments']}), 
    ]

    #prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'user','category','pub_date')
    list_filter = ['pub_date']
    search_fields = ['title','user' ,'summary', 'content']
    date_hierarchy = 'pub_date'
    
    



admin.site.register(Blog,BlogAdmin)
admin.site.register(Category)