from django.db import models

# Create your models here.
class Faq(models.Model):
    title         = models.CharField(max_length=200)
    pub_date      = models.DateTimeField('date published')
    content       = models.TextField()
    slug          = models.SlugField(max_length=50)
    
    class Meta:
		verbose_name = "Faq"
		verbose_name_plural = "Faqs"
		
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/faq/%s/" % (self.slug)