from django.conf import settings
from django import template
from link.models import Link, Category
from django.shortcuts import get_object_or_404
register = template.Library()


@register.tag
def get_links(parser, token):
	"""
		{% get_links 5 as links_items %}
	"""
	bits = token.split_contents()
	if len(bits) == 3:
		limit = None
	elif len(bits) == 4:
		try:
			limit = abs(int(bits[1]))
		except ValueError:
			raise template.TemplateSyntaxError("If provided, second argument to `get_links` must be a positive whole number.")
	if bits[-2].lower() != 'as':
		raise template.TemplateSyntaxError("Missing 'as' from 'get_links' template tag.  Format is {% get_links 5 as links_items %}.")
	return LinkItemNode(bits[-1], limit)

		
class LinkItemNode(template.Node):
	"""
	Returns a QuerySet of published LinkItems based on the lookup parameters.
	"""
	
	def __init__(self, varname, limit=None, author=None, category_slug=None, filters=None):
		self.varname = varname
		self.limit = limit
		self.filters = filters
		# author is either a literal NewsAuthor slug,
		# or a template variable containing a NewsAuthor slug.
		self.author = author
		self.category = category_slug
		
	def render(self, context):
		# Base QuerySet, which will be filtered further if necessary.
		links = Link.objects.all()
		
		# Do we filter by author?  If so, first attempt to resolve `author` as
		# a template.Variable.  If that doesn't work, use `author` as a literal
		# NewsAuthor.slug lookup.
		if self.author is not None:
			try:
				author_slug = template.Variable(self.author).resolve(context)
			except template.VariableDoesNotExist:
				author_slug = self.author
			links = links.filter(author__slug=author_slug)
			
		if self.category is not None:
			try:
				category_slug = template.Variable(self.category).resolve(context)
			except template.VariableDoesNotExist:
				category_slug = self.category
			links = links.filter(category__slug=category_slug)
			
			
		# Apply any additional lookup filters
		if self.filters:
			links = links.filter(**self.filters)
			
		# Apply a limit.
		if self.limit:
			links = links[:self.limit]
			
		context[self.varname] = links
		return u''


def parse_token(token):
	"""
	Parses a token into 'slug', 'limit', and 'varname' values.
	Token must follow format {% tag_name <slug> [<limit>] as <varname> %}
	"""
	bits = token.split_contents()
	if len(bits) == 5:
		# A limit was passed it -- try to parse / validate it.
		try:
			limit = abs(int(bits[2]))
		except:
			limit = None
	elif len(bits) == 4:
		# No limit was specified.
		limit = None
	else:
		# Syntax is wrong.
		raise template.TemplateSyntaxError("Wrong number of arguments: format is {%% %s <slug> [<limit>] as <varname> %%}" % bits[0])
	if bits[-2].lower() != 'as':
		raise template.TemplateSyntaxError("Missing 'as': format is {%% %s <slug> [<limit>] as <varname> %%}" % bits[0])
	return (bits[1], limit, bits[-1])


@register.tag
def get_links_by_user(parser,token):
	"""
	{% get_links_by_user <slug> [<limit>] as <varname> %}
		{% get_links_by_user foo 5 as links_items %}	# 5 articles
		{% get_links_by_user foo as links_items %}	# all articles
	"""
	author_slug, limit, varname = parse_token(token)
	return LinkItemNode(varname, limit, author=author_slug)

	
@register.tag
def get_links_by_category(parser,token):
	"""
	{% get_links_by_category <slug> [<limit>] as <varname> %}
		{% get_links_by_category foo 5 as links_items %}	# 5 articles
		{% get_links_by_category foo as links_items %}	# all articles
	"""
	category_slug, limit, varname = parse_token(token)
	return LinkItemNode(varname, limit, category_slug=category_slug)
	
@register.tag
def get_urls_by_category(parser,token):
	"""
	This is because I got sick of having to debug issues due to the fact that I typed one or the other.
	"""
	return get_links_by_category(parser,token)

	
@register.tag
def get_links_by_tag(parser,token):
	"""
	{% get_posts_by_tag <tag> [<limit>] as <varname> %}
	"""
	tag, limit, varname = parse_token(token)
	return LinkItemNode(varname, limit, filters={'tags__contains':tag})

		
@register.tag
def months_with_links(parser, token):
	"""
		{% months_with_links 4 as months %}
	"""
	bits = token.split_contents()
	if len(bits) == 3:
		limit = None
	elif len(bits) == 4:
		try:
			limit = abs(int(bits[1]))
		except ValueError:
			raise template.TemplateSyntaxError("If provided, second argument to `months_with_news` must be a positive whole number.")
	if bits[-2].lower() != 'as':
		raise template.TemplateSyntaxError("Missing 'as' from 'months_with_news' template tag.  Format is {% months_with_news 5 as months %}.")
	return MonthNode(bits[-1], limit=limit)
	
	
class MonthNode(template.Node):
	
	def __init__(self,varname,limit=None):
		self.varname = varname
		self.limit = limit	# for MonthNode inheritance
	
	def render(self, context):
		try:
			months = Link.objects.get_published().dates('date', 'month', order="DESC")
		except:
			months = None
		if self.limit is not None:
			months = list(months)
			months = months[:self.limit]
		context[self.varname] = months
		return ''