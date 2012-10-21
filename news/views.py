# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: views.py
# Creation Date: 2011-11-04  16:38
# Last Modified: 2011-11-12 17:21:50
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.db.models.query import EmptyQuerySet
from django.db.models import Q


from django.views.generic import DetailView, ListView
from django.views.generic import YearArchiveView
from django.views.generic import DateDetailView
                                        
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import get_object_or_404

# ------------------------------------------------------------

# 3dpart.
from photologue.models import Photo
# ------------------------------------------------------------

# ddtcms.
from ddtcms.news.models import News
from ddtcms.news.models import Category
from ddtcms.news.models import NewsPhotoGallery
from ddtcms.news.forms  import NewsForm
from ddtcms.news.signals import latest_news_created
# ------------------------------------------------------------

# config.
#
# ------------------------------------------------------------

def by_tag(request,tag):
    qs = News.objects.all().filter(tags__contains=tag,pub_date__isnull=False)
    return ListView.as_view(request,qs,template_object_name='item')
    
def by_category(request,category_slug):
    #raise Http404(category_slug)
    
    category = get_object_or_404(Category.objects.all(), slug=category_slug)
    
    the_parent = category.parent
    
    #qs = News.objects.all().filter(category=the_category,pub_date__isnull=False)
    qs = News.objects.for_categories(category=category)
    
    if the_parent:
        child_categories=the_parent.get_children()
    else:
        child_categories=category.get_children()
        
    latest_news      = News.objects.get_published()[:10]
    most_viewed_news = News.objects.get_published().order_by('-views')[:10]
    recommended_news = News.objects.get_recommended()[:5]
        
    return ListView.as_view(request,qs,template_object_name='item',paginate_by=10,
                        extra_context=locals())
    
def category_list(request,empty_arg):
    return ListView.as_view(request,Category.objects.all(),template_object_name='item')
    
#def by_author(request,author_slug):
#   the_author = get_object_or_404(NewsAuthor.on_site, slug=author_slug)
#   qs = NewsItem.on_site.filter(author=the_author,date__isnull=False)
#   return ListView.as_view(request,qs,template_object_name='item')
#   
#def author_list(request):
#   return ListView.as_view(request,NewsAuthor.on_site.all(),template_object_name='item')


def by_year(request,year):
   qs = News.objects.all()
   return YearArchiveView.as_view(request,year,qs,date_field='pub_date',template_object_name='item',make_object_list=True)
   
def index(request):
    news_count       = News.objects.all().count()
    news_list        = News.objects.get_published()[:10]
        
    latest_news      = News.objects.get_published()[:10]
    recommended_news = News.objects.get_recommended()[:5]
    flashslide_news  = News.objects.get_flashslide()[:4]
    headline_news_list    = News.objects.get_headlines()[1:4]
    most_viewed_news = News.objects.get_published().order_by('-views')[:10]
    most_commented_news = News.objects.get_published().order_by('-comments')[:6]
    try:
        top_headline    = News.objects.get_headlines().latest()
    except News.DoesNotExist:
        top_headline = None
    
    categories       = Category.objects.all().filter(parent__exact=None)
    return render_to_response('news/news_index.html', locals(),
                              context_instance=RequestContext(request))
        
 
class CategoryNewsListView(DetailView):

    template_object_name='item'
    paginate_by=10 
    context_object_name = "news_list"
    template_name = "news/news_by_category.html",
    model=Category
    
    def get_queryset(self):
        #r,a,k=self.request,self.args,self.kwargs
        self.category = get_object_or_404(Category, slug__iexact=self.kwargs['slug'])
        #self.category = self.object # cannot work
        #b()
        #return News.objects.for_categories(category=category)
        return News.objects.filter(category=self.category)

    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryNewsListView, self).get_context_data(**kwargs)
        
        the_category = self.category
        the_parent   = the_category.parent
        
        if the_parent:
            child_categories=the_parent.get_children()
        else:
            child_categories=the_category.get_children()
            
        context['most_viewed_news'] = News.objects.get_published().order_by('-views')[:10]
        context['recommended_news'] = News.objects.get_recommended()[:5]
        context['child_categories'] = child_categories
        context['latest_news']      = News.objects.get_published()[:10]
        
        context['category']      = self.category
            
        return context



class NewsDetailView(DateDetailView):

    queryset            = News.objects.all()
    model               = News,
    context_object_name = 'news',

    def get_object(self):
        # Call the superclass
        object = super(NewsDetailView, self).get_object()
        # Record the last accessed date
        object.views += 1
        object.save()
        # Return the object
        return object

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        
        #the_category = get_object_or_404(Category.objects.all(), slug=self.object.category.slug)
        the_category = self.object.category
        
        the_parent   = the_category.parent
        
        if the_parent:
            child_categories=the_parent.get_children()
        else:
            child_categories=the_category.get_children()
            
        context['most_viewed_news'] = News.objects.get_published().order_by('-views')[:10]
        context['recommended_news'] = News.objects.get_recommended()[:5]
        context['child_categories'] = child_categories
        context['latest_news']      = News.objects.get_published()[:6]
        
        
        return context



@login_required
def post(request, category = "", success_url=None,
             form_class=NewsForm,
             template_name='news/news_post.html',
             extra_context=None):   
    
    if category != "":
        c = get_object_or_404(Category.objects.all(), slug=category)
    else:
        c = None
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.deliverer = request.user
            instance.save()
            form.save_m2m()

            #kwargs = {}
            #kwargs['title']   = _("%s Posted A new News: %s") % (self.deliverer.username,self.title)
            #kwargs['content'] = _("%s Posted A new News,go and view it now <a href='%s'> %s </a> " ) % (self.deliverer.username,self.get_absolute_url(),self.title)
            #kwargs['slug']    = "news%d-%s" % (self.id,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            #latest_news_created.send(sender=self.__class__,**kwargs)
            
            if form.files:
                gallery = NewsPhotoGallery.objects.create(
                    title = "%s-%d" % (instance.title,instance.id),
                    title_slug ="%s-%d" %  (instance.slug,instance.id),
                    description = instance.title,
                    date_added = instance.pub_date,
                    tags = instance.tags
                )
                instance.gallery = gallery
                instance.save()

                counter = 1
                photofile_fieldlist=form.files.keys()
                #d()
                #for photofilefield in form.files:
                for photofilefield in sorted(photofile_fieldlist):
                    photo_file = form.files[photofilefield]
                    photo = Photo(title = '-'.join([gallery.title, str(counter)]),
                                title_slug ='-'.join([gallery.title_slug, str(gallery.id) , 'p', str(counter)]),
                                caption = gallery.description,
                                tags = gallery.tags)
                    photo.image.save(photo_file.name, photo_file)
                    gallery.photos.add(photo)
                    counter = counter + 1
    
                    if photofilefield == u"file":
                        if not gallery.cover:
                            gallery.cover = photo
                            gallery.save()

            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        #initial={'category':c.id, 'deliverer':request.user.id}
        initial={'deliverer':request.user.id}
        form = form_class(initial=initial)
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form,
                                'category':c,
                              },
                              context_instance=context)

def search(request,keywords=None):
    if not keywords:
        keywords = request.GET.get('q', "")
    if keywords != "":
        qs=News.objects.get_published().filter(Q(title__contains = keywords) | Q(content__contains = keywords))
    else:
        qs=EmptyQuerySet()
    
    return ListView.as_view(request,qs,
                       template_object_name='item',
                       template_name='news/search.html',
                       paginate_by=1,
                       extra_context={"keywords":keywords})