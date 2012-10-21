# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: models.py
# Creation Date: 2011-11-05  02:22
# Last Modified: 2011-11-12 17:19:35
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import datetime
#import urllib
# ------------------------------------------------------------

# django.
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.template.defaultfilters import slugify
# ------------------------------------------------------------

# 3dpart.
from tagging.fields import TagField
tagfield_help_text = _('Separate tags with spaces, put quotes around multiple-word tags.')
from photologue.models import Gallery, Photo
# ------------------------------------------------------------

# ddtcms.
from news.managers import CategoryManager
from news.managers import NewsManager
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------

class Category(models.Model):
	name          = models.CharField(_('name'), max_length=50)
	slug          = models.SlugField(max_length=50,unique=True,help_text='alias to the name,use english')
	parent        = models.ForeignKey('self',null=True,blank=True,related_name='child')
	depth         = models.PositiveSmallIntegerField(_("category's depth"), blank=True,null=True)
	path          = models.CharField(_("category's path"),blank=True,null=True, max_length=250, editable=False)
	posts         = models.IntegerField(_("News Posts Count"), default=0)
	order         = models.PositiveSmallIntegerField(_('order'), default=0)

	objects       = CategoryManager()


	class Meta:
		ordering            =  ('parent__id','order','slug',)
		verbose_name        = _('News Category')
		verbose_name_plural = _('News Categories')

	def __unicode__(self):
		return self.name

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
			self.slug = self.slug.lower().replace('-','_')

		p_list = self._recurse_for_parents_id(self)
		p_list.append(self.id)
		self.depth = len(p_list)
		self.path = '/'.join(map(str, p_list))
		super(Category,self).save(*args,**kwargs)
		
		#if not self.path:
		#	p_list = self._recurse_for_parents_id(self)
		#	p_list.append(self.id)
		#	#self.path = '%s' % '/'.join (p_list)
		#	#self.path = '/'.join (p_list)
		#	self.depth = len(p_list)
		#	self.path = '/'.join(map(str, p_list))
		#self.save()
		#if not self.depth:
		#    p_list = self.path.split('/')
		#    self.depth = len(p_list)
		#     self.save()



	def is_root(self):
		if self.parent == None:
			return True
		return False

	def get_root(self):
		p = self.parent
		if p:
			p=p.get_root()
		else:
			p=self
		return p

	def get_depth(self):
		if not self.depth:
			p_list = self.path.split('/')
			self.depth = len(p_list)
			self.save()
		return self.depth

	def _recurse_for_parents_id(self, category_obj):
		#This is used for the urls
		p_list = []
		if category_obj.parent_id:
			p = category_obj.parent
			p_list.append(p.id)
			more = self._recurse_for_parents_id(p)
			p_list.extend(more)
		if category_obj == self and p_list:
			p_list.reverse()
		return p_list

	def _recurse_for_parents_slug(self, category_obj):
		#This is used for the urls
		p_list = []
		if category_obj.parent_id:
			p = category_obj.parent
			p_list.append(p.slug)
			more = self._recurse_for_parents_slug(p)
			p_list.extend(more)
		if category_obj == self and p_list:
			p_list.reverse()
		return p_list

	#def get_absolute_url(self):
	#   return "/news/category/%s/" %  self.slug
	def get_absolute_url(self):
		p_list = self._recurse_for_parents_slug(self)
		p_list.append(self.slug)
		return '%s%s/' % (reverse('news_index'), '/'.join (p_list))

	def _recurse_for_parents_name_url(self, category__obj):
		#Get all the absolute urls and names (for use in site navigation)
		p_list = []
		url_list = []
		if category__obj.parent_id:
			p = category__obj.parent
			p_list.append(p.name)
			url_list.append(p.get_absolute_url())
			more, url = self._recurse_for_parents_name_url(p)
			p_list.extend(more)
			url_list.extend(url)
		if category__obj == self and p_list:
			p_list.reverse()
			url_list.reverse()
		return p_list, url_list

	def get_url_name(self):
		#Get a list of the url to display and the actual urls
		p_list, url_list = self._recurse_for_parents_name_url(self)
		p_list.append(self.name)
		url_list.append(self.get_absolute_url())
		return zip(p_list, url_list)

	def _flatten(self, L):
		"""
		Taken from a python newsgroup post
		"""
		if type(L) != type([]): return [L]
		if L == []: return L
		return self._flatten(L[0]) + self._flatten(L[1:])

	def _recurse_for_children(self, node):
		children = []
		children.append(node)
		for child in node.child.all():
			children_list = self._recurse_for_children(child)
			children.append(children_list)
		return children

	def get_all_children(self):
		"""
		Gets a list of all of the children.
		"""
		children_list = self._recurse_for_children(self)
		flat_list = self._flatten(children_list[1:])
		return flat_list

	def get_children(self):
		return self.child.all()

	def has_children(self):
		if self.get_children():
			return True
		else:
			return False

	def total_posts(self):
		total=0
		if not self.get_children():
			total = self.posts
		else:
			for c in self.get_all_children():
				total += c.posts
		return total

class Source(models.Model):
    """
    A source is a general news source, like CNN, who may provide multiple feeds.
    """
    name        = models.CharField(max_length=255)
    url         = models.URLField()
    description = models.TextField(blank=True)
    logo        = models.ImageField(blank=True, upload_to='images/news_logos')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name



class NewsPhotoGallery(Gallery):
	pass



NEWS_STATUS = (
(0,  _('NORMAL')),
(1,  _('HEADLINE')),
(2,  _('RECOMMENDED')),
(3,  _('FLASHSLIDE')),
(9,  _('DELETED')),
)



class News(models.Model):
	category       = models.ForeignKey(Category,null=True)
	deliverer      = models.ForeignKey(User,verbose_name='Deliverer',null=True,editable=True)
	source         = models.CharField(verbose_name='News Source',max_length=50,null=True,blank=True,help_text='Where the news comes from')
	title          = models.CharField(max_length=100)
	subtitle       = models.CharField(max_length=100,null=True,blank=True)
	slug           = models.SlugField(max_length=255,blank=True,unique=True,help_text='Automatically built From the title.')
	pub_date       = models.DateTimeField('date published',blank=True,default=datetime.datetime.now)
	content        = models.TextField()
	summary        = models.TextField(help_text="Summary",null=True,blank=True)
	tags           = TagField(help_text=tagfield_help_text, verbose_name=_('tags'))
	views          = models.PositiveIntegerField(_("Views"), default=0)
	comments       = models.PositiveIntegerField(_("Comments"), default=0)
	allow_comments = models.BooleanField(_("Allow Comments"),default=True)
	gallery        = models.ForeignKey(NewsPhotoGallery, unique=True, verbose_name=_('gallery'),related_name='gallery_news2',null=True,blank=True)
	approved       = models.BooleanField(_("Approved"),default=False)
	pic            = models.CharField('News Indicator Pic',max_length=200,null=True,blank=True,help_text="If has a pic url,show on homepage or indexpage")
	status         = models.PositiveIntegerField(_("Status"), choices=NEWS_STATUS, default=0)
	editor         = models.CharField(max_length=20,blank=True)


	objects = NewsManager()


	class Meta:
		ordering            = ('-pub_date',)
		unique_together     = (('slug', 'pub_date'), )
		get_latest_by       = 'pub_date'
		verbose_name        = _('News')
		verbose_name_plural = _('News')

	def get_absolute_url(self):
		if self.slug=="":
			return "/news/%s/" % self.id
		else:
			#return "/news/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
			return "/news/%s/%s/" % (self.pub_date.strftime("%Y/%m/%d").lower(), self.slug)

	def __unicode__(self):
		return self.title

	def get_previous(self):
		try:
			# isnull is to check whether it's published or not - drafts don't have dates, apparently
			return News.objects.all().filter(pub_date__lt=self.pub_date,pub_date__isnull=False)[0]
		except IndexError, e:
			# print 'Exception: %s' % e.message
			return None

	def get_next(self):
		try:
			# isnull is to check whether it's published or not - drafts don't have dates, apparently
			return News.objects.all().filter(pub_date__gt=self.pub_date,pub_date__isnull=False).order_by('pub_date')[0]
		except IndexError, e:
			# print 'Exception: %s' % e.message
			return None

	def approved_comments(self):
		return Comment.objects.for_model(self).filter(is_public=True)

	def unapproved_comments(self):
		return Comment.objects.for_model(self).filter(is_public=False)

	def total_comments(self):
		return Comment.objects.for_model(self)


	def today_posts(self):
		ps = []
		return 0

	def is_pic(self):
		return (not self.photo_count() == 0)

	def get_photos(self):
		try:
			photos = self.gallery.photos.all().order_by('title_slug')
		except AttributeError:
			photos = []
		return photos

	def photo_count(self):
		if self.gallery:
			return self.gallery.photo_count
		else:
			return 0

	def get_cover(self):
		cover = None
		if self.gallery:
			cover = self.gallery.cover
		return cover

	def save(self,*args,**kwargs):
		#if not self.slug:
		#self.slug = slugify(self.title)
		#self.slug = self.slug.lower().replace('-','_')
		from ddtcms.utils.convert import CConvert
		utf8String = self.title
		convert   = CConvert()
		#convert.just_shengmu=True
		#convert.spliter=" "
		self.slug = convert.convert(utf8String)
		#self.slug = self.slug.lower().replace('-','_')
		self.slug = self.slug.lower()
		super(News,self).save(*args,**kwargs)


		c       = self.category
		c.posts = c.news_set.count()
		c.save()



	#def send_latest_to_notice(self,title,pub_date,over_date,content,slug):
	#	latest_news_added.send(sender=self, title=title,pub_date=pub_date,over_date=over_date,content=content,slug=slug)




class NewsPackageUpload(models.Model):
    zip_file    = models.FileField(_('zip file (.zip)'), upload_to="upload/temp",
                                help_text=_('Select a .zip file of news to upload into a new Category.'))
    category    = models.ForeignKey(Category, null=True, blank=True, help_text=_('Select a category to add a news to.'))

    class Meta:
        verbose_name        = _('group file (.zip) upload')
        verbose_name_plural = _('group file (.zip) uploads')

    def save(self, *args, **kwargs):
        super(NewsPackageUpload, self).save(*args, **kwargs)
        category = self.process_zipfile()
        super(NewsPackageUpload, self).delete()
        return category

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip      = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            if self.category:
                category = self.category
            else:
                raise Exception('must choose a category')

            for filename in sorted(zip.namelist()):
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django.newforms.fields.ImageField:
                        #  load() is the only method that can spot a truncated JPEG,
                        #  but it cannot be called sanely after verify()
                        trial_image = Image.open(StringIO(data))
                        trial_image.load()
                        # verify() is the only method that can spot a corrupt PNG,
                        #  but it must be called immediately after the constructor
                        trial_image = Image.open(StringIO(data))
                        trial_image.verify()
                    except Exception:
                        # if a "bad" file is found we just skip it.
                        continue
                    while 1:
                        title = ' '.join([self.title, str(count)])
                        slug = slugify(title)
                        try:
                            p = Photo.objects.get(title_slug=slug)
                        except Photo.DoesNotExist:
                            photo = Photo(title      = title,
                                          title_slug = slug,
                                          caption    = self.caption,
                                          is_public  = self.is_public,
                                          tags       = self.tags)
                            photo.image.save(filename, ContentFile(data))
                            gallery.photos.add(photo)
                            count = count + 1
                            break
                        count = count + 1
            zip.close()
            return gallery



            for key in d.keys():
                if key[0:4]=='name':
                    #i=int(key[4:])
                    #print d[key],'=',d['url'+key[4:]]
                    title = d[key]
                    try:
                        url   = d['url'+key[4:]]
                    except KeyError:
                        continue

                    link=Link(
                        title    = title,
                        category = category,
                        url      = url,
                        notes    = title,
                        pub_date = datetime.date.today(),
                    )
                    link.save()

            return category