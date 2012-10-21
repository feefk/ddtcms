from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from member.forms import AvatarForm, AvatarCropForm, EmailValidationForm, \
                              ProfileForm, _RegistrationForm, LocationForm, \
                              ResendEmailValidationForm, PublicFieldsForm
from member.models import BaseProfile, DEFAULT_AVATAR_SIZE, MIN_AVATAR_SIZE, \
        SAVE_IMG_PARAMS, DEFAULT_AVATAR
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.db import models
from django.contrib.auth.models import User, SiteProfileNotAvailable
from member.models import EmailValidation, Avatar, UserProfileMediaNotFound, \
                               GoogleDataAPINotFound, S3BackendNotFound
from django.template import RequestContext
from cStringIO import StringIO
from django.core.files.base import ContentFile
import urlparse
from django.conf import settings
from xml.dom import minidom
import urllib2
import random
import cPickle as pickle
import base64
import urllib
import os
from member import signals
import copy
from django.contrib import messages
from django.utils.encoding import iri_to_uri

if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
    from backends.S3Storage import S3Storage

if hasattr(settings, "AVATAR_QUOTA"):
    from userprofile.uploadhandler import QuotaUploadHandler

try:
    from PIL import Image
except ImportError:
    import Image

if not settings.AUTH_PROFILE_MODULE:
    raise SiteProfileNotAvailable
try:
    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    Profile = models.get_model(app_label, model_name)
except (ImportError, ImproperlyConfigured):
    raise SiteProfileNotAvailable

if not Profile:
    raise SiteProfileNotAvailable

if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, "upload/member")):
    raise UserProfileMediaNotFound

GOOGLE_MAPS_API_KEY = hasattr(settings, "GOOGLE_MAPS_API_KEY") and \
                      settings.GOOGLE_MAPS_API_KEY or None
AVATAR_WEBSEARCH = hasattr(settings, "AVATAR_WEBSEARCH") and \
                   settings.AVATAR_WEBSEARCH or None

if AVATAR_WEBSEARCH:
    try:
        import gdata.service
        import gdata.photos.service
    except:
        raise GoogleDataAPINotFound

def get_profiles():
    return Profile.objects.order_by("-date").all()[:64]

def fetch_geodata(request, lat, lng):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        url = "http://ws.geonames.org/countrySubdivision?lat=%s&lng=%s" % (lat, lng)
        dom = minidom.parse(urllib.urlopen(url))
        country = dom.getElementsByTagName('countryCode')
        if len(country) >=1:
            country = country[0].childNodes[0].data
        region = dom.getElementsByTagName('adminName1')
        if len(region) >=1:
            region = region[0].childNodes[0].data

        return HttpResponse(simplejson.dumps({'success': True, 'country': country, 'region': region}))
    else:
        raise Http404()

def public(request, username):
    try:
        profile = User.objects.get(username=username).get_profile()
    except:
        raise Http404

    template = "member/profile/public.html"
    data = { 'profile': profile, 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY, 'DEFAULT_AVATAR_SIZE': DEFAULT_AVATAR_SIZE }
    signals.context_signal.send(sender=public, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def overview(request):
    """
    Main profile page
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    validated = False
    try:
        email = EmailValidation.objects.exclude(verified=True).get(user=request.user).email
    except EmailValidation.DoesNotExist:
        email = request.user.email
        if email: validated = True

    fields = [{ 
        'name': f.name, 
        'verbose_name': f.verbose_name, 
        'value': getattr(profile, f.name)
    } for f in Profile._meta.fields if not (f in BaseProfile._meta.fields or f.name=='id')]

    template = "member/profile/overview.html"
    data = { 'section': 'overview', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
            'email': email, 'validated': validated, 'fields' : fields, 'DEFAULT_AVATAR_SIZE': DEFAULT_AVATAR_SIZE }
    signals.context_signal.send(sender=overview, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def personal(request):
    """
    Personal data of the user profile
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        old_profile = copy.copy(profile)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile information has been updated successfully."), fail_silently=True)
            signal_responses = signals.post_signal.send(sender=personal, request=request, form=form, extra={'old_profile':old_profile})
            last_response = signals.last_response(signal_responses)
            if last_response:
                return last_response
    else:
        form = ProfileForm(instance=profile)

    template = "member/profile/personal.html"
    data = { 'section': 'personal', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
             'form': form, }
    signals.context_signal.send(sender=personal, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def location(request):
    """
    Location selection of the user profile
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    geoip = hasattr(settings, "GEOIP_PATH")
    if geoip and request.method == "GET" and request.GET.get('ip') == "1":
        from django.contrib.gis.utils import GeoIP
        g = GeoIP()
        c = g.city(request.META.get("REMOTE_ADDR"))
        if c and c.get("latitude") and c.get("longitude"):
            profile.latitude = "%.6f" % c.get("latitude")
            profile.longitude = "%.6f" % c.get("longitude")
            profile.country = c.get("country_code")
            profile.location = unicode(c.get("city"), "latin1")

    if request.method == "POST":
        form = LocationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile information has been updated successfully."), fail_silently=True)

            signal_responses = signals.post_signal.send(sender=location, request=request, form=form)
            last_response = signals.last_response(signal_responses)
            if last_response:
                return last_response

    else:
        form = LocationForm(instance=profile)

    template = "member/profile/location.html"
    data = { 'section': 'location', 'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
             'form': form, 'geoip': geoip }
    signals.context_signal.send(sender=location, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def delete(request):
    if request.method == "POST":
        profile, created = Profile.objects.get_or_create(user=request.user)
        old_profile = copy.copy(profile)
        old_user    = copy.copy(request.user)

        # Remove the profile and all the information
        Profile.objects.filter(user=request.user).delete()
        EmailValidation.objects.filter(user=request.user).delete()
        Avatar.objects.filter(user=request.user).delete()

        # Remove the e-mail of the account too
        request.user.email = ''
        request.user.first_name = ''
        request.user.last_name = ''
        request.user.save()

        messages.success(request, _("Your profile information has been removed successfully."), fail_silently=True)

        signal_responses = signals.post_signal.send(sender=delete, request=request, extra={'old_profile':old_profile, 'old_user': old_user})
        return signals.last_response(signal_responses) or HttpResponseRedirect(reverse("profile_overview"))

    template = "member/profile/delete.html"
    data = { 'section': 'delete', }
    signals.context_signal.send(sender=delete, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def avatarchoose(request):
    """
    Avatar choose
    """
    profile, created = Profile.objects.get_or_create(user = request.user)
    images = dict()

    if hasattr(settings, "AVATAR_QUOTA"):
        request.upload_handlers.insert(0, QuotaUploadHandler())

    if request.method == "POST":
        form = AvatarForm()
        if request.POST.get('keyword'):
            keyword = iri_to_uri(request.POST.get('keyword'))
            gd_client = gdata.photos.service.PhotosService()
            feed = gd_client.SearchCommunityPhotos(query = "%s&thumbsize=72c" % keyword.split(" ")[0], limit='48')
            for entry in feed.entry:
                images[entry.media.thumbnail[0].url] = entry.content.src

        else:
            form = AvatarForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('url') or form.cleaned_data.get('photo')
                try:
                    thumb = Image.open(ContentFile(image.read()))
                except:
                    messages.error(request, _("This image can't be used as an avatar"))
                else:
                    thumb.thumbnail((480, 480), Image.ANTIALIAS)
                    f = StringIO()
                    save_img_params = SAVE_IMG_PARAMS.get(thumb.format, {})
                    try:
                        thumb.save(f, thumb.format, **SAVE_IMG_PARAMS.get(thumb.format, {}))
                    except:
                        thumb.save(f, thumb.format)
                    f.seek(0)
                    avatar = Avatar(user=request.user, image="", valid=False)
                    file_ext = image.content_type.split("/")[1] # "image/gif" => "gif"
                    if file_ext == 'pjpeg':
                        file_ext = 'jpeg'
                    avatar.image.save("%s.%s" % (request.user.username, file_ext), ContentFile(f.read()))
                    avatar.save()

                    signal_responses = signals.post_signal.send(sender=avatarchoose, request=request, form=form)
                    return signals.last_response(signal_responses) or HttpResponseRedirect(reverse("profile_avatar_crop"))

    else:
        form = AvatarForm()

    if DEFAULT_AVATAR:
        base, filename = os.path.split(DEFAULT_AVATAR)
        filename, extension = os.path.splitext(filename)
        generic = "%s/%s.%d%s" % (base, filename, DEFAULT_AVATAR_SIZE, extension)
        generic = generic.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    else:
        generic = ""

    template = "member/avatar/choose.html"
    data = { 'generic': generic, 'form': form, "images": images,
             'AVATAR_WEBSEARCH': AVATAR_WEBSEARCH, 'section': 'avatar',
             'DEFAULT_AVATAR_SIZE': DEFAULT_AVATAR_SIZE, 'MIN_AVATAR_SIZE': MIN_AVATAR_SIZE }
    signals.context_signal.send(sender=avatarchoose, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def avatarcrop(request):
    """
    Avatar management
    """
    avatar = get_object_or_404(Avatar, user=request.user, valid=False)
    if not request.method == "POST":
        form = AvatarCropForm()
    else:
        image = Image.open(ContentFile(avatar.image.read()))
        form = AvatarCropForm(image, request.POST)
        if form.is_valid():
            top = int(form.cleaned_data.get('top'))
            left = int(form.cleaned_data.get('left'))
            right = int(form.cleaned_data.get('right'))
            bottom = int(form.cleaned_data.get('bottom'))

            if not (top or left or right or bottom):
                (width, height) = image.size
                if width > height:
                    diff = (width-height) / 2
                    left = diff
                    right = width-diff
                    bottom = height
                else:
                    diff = (height-width) / 2
                    top = diff
                    right = width
                    bottom = height-diff

            box = [ left, top, right, bottom ]
            image = image.crop(box)

            if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
                f = StringIO()
                image.save(f, image.format)
                f.seek(0)
                avatar.image.delete()
                file_ext = image.content_type.split("/")[1] # "image/gif" => "gif"
                if file_ext == 'pjpeg':
                    file_ext = 'jpeg'
                avatar.image.save("%s.%s" % (request.user.username, file_ext), ContentFile(f.read()))
            else:
                image.save(avatar.image.path)

            avatar.valid = True
            avatar.save()
            messages.success(request, _("Your new avatar has been saved successfully."), fail_silently=True)

            signal_responses = signals.post_signal.send(sender=avatarcrop, request=request, form=form)
            return signals.last_response(signal_responses) or HttpResponseRedirect(reverse("profile_edit_avatar"))

    template = "member/avatar/crop.html"
    data = { 'section': 'avatar', 'avatar': avatar, 'form': form, \
        'DEFAULT_AVATAR_SIZE': DEFAULT_AVATAR_SIZE, 'MIN_AVATAR_SIZE': MIN_AVATAR_SIZE }
    signals.context_signal.send(sender=avatarcrop, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def avatardelete(request, avatar_id=False):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            for avatar in Avatar.objects.filter(user=request.user):
                avatar.delete()
            return HttpResponse(simplejson.dumps({'success': True}))
        except:
            return HttpResponse(simplejson.dumps({'success': False}))
    else:
        raise Http404()

def email_validation_process(request, key):
    """
    Verify key and change email
    """
    if EmailValidation.objects.verify(key=key):
        successful = True
    else:
        successful = False

    signal_responses = signals.post_signal.send(sender=email_validation_process, request=request, extra={'key': key, 'successful': successful})
    last_response = signals.last_response(signal_responses)
    if last_response:
        return last_response

    template = "member/account/email_validation_done.html"
    data = { 'successful': successful, }
    signals.context_signal.send(sender=email_validation_process, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def email_validation(request):
    """
    E-mail Change form
    """
    if request.method == 'POST':
        form = EmailValidationForm(request.POST)
        if form.is_valid():
            EmailValidation.objects.add(user=request.user, email=form.cleaned_data.get('email'))

            signal_responses = signals.post_signal.send(sender=email_validation, request=request, form=form)
            return signals.last_response(signal_responses) or HttpResponseRedirect(reverse("email_validation_processed"))
    else:
        form = EmailValidationForm()

    template = "member/account/email_validation.html"
    data = { 'form': form, }
    signals.context_signal.send(sender=email_validation, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = _RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            newuser = Profile.objects.create_user(username=username, email='', password=password)
            newuser.is_active = not hasattr(settings, "REQUIRE_EMAIL_CONFIRMATION") or not settings.REQUIRE_EMAIL_CONFIRMATION

            if form.cleaned_data.get('email'):
                newuser.email = form.cleaned_data.get('email')
                EmailValidation.objects.add(user=newuser, email=newuser.email)

            newuser.save()
            #return HttpResponseRedirect('%scomplete/' % request.path_info)
            #template_name='member/account/registration_done.html'
            #data={'username': username}
            #return render_to_response(template_name,
            #                  data,
            #                  context_instance=RequestContext(request))
            
            return HttpResponseRedirect(reverse("signup_complete", args=[username]))
    else:
        form = _RegistrationForm()

    template = "member/account/registration.html"
    data = { 'form': form, }
    signals.context_signal.send(sender=register, request=request, context=data)
    return render_to_response(template, data, context_instance=RequestContext(request))


def register_complete(request,username,template_name='member/account/registration_done.html',extra_context=None):
    #if request.method == 'POST':
    #    data = {'username':"aas1111111"}
    #    pass

    #else:
    #    pass
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    data = {'username': username}
    return render_to_response(template_name,
                              data,
                              context_instance=context)



def email_validation_reset(request):
    """
    Resend the validation email
    """

    if request.user.is_authenticated():
        try:
            resend = EmailValidation.objects.exclude(verified=True).get(user=request.user).resend()
            response = "done"
        except EmailValidation.DoesNotExist:
            response = "failed"

        signal_responses = signals.post_signal.send(sender=email_validation_reset, request=request, extra={'response': response})
        return signals.last_response(signal_responses) or HttpResponseRedirect(reverse("email_validation_reset_response", args=[response]))

    else:
        if request.method == 'POST':
            form = ResendEmailValidationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                try:
                    resend = EmailValidation.objects.exclude(verified=True).get(email=email).resend()
                    response = "done"
                except EmailValidation.DoesNotExist:
                    response = "failed"

                signal_responses = signals.post_signal.send(sender=email_validation_reset, request=request, extra={'response': response})
                return signals.last_response(signal_responses) or HttpResponseRedirect(reverse("email_validation_reset_response", args=[response]))

        else:
            form = ResendEmailValidationForm()

        template = "member/account/email_validation_reset.html"
        data = { 'form': form, }
        signals.context_signal.send(sender=email_validation_reset, request=request, context=data)
        return render_to_response(template, data, context_instance=RequestContext(request))

def ajax_loginsta(request):
    """
    ajax_loginsta
    """
    user = request.user
    logined = request.user.is_authenticated()    
    
    template = "member/profile/ajax_userstate.html"
    data = { 'user': user, }
    
     
    if logined:
        rendered = render_to_string(template, data) 
        response = HttpResponse()
        
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'no-cache'
        response['Expires'] = 0  
        
        response.content = rendered
    else:
        rendered =''
        response = HttpResponseForbidden() 
        response.content = rendered 
        response['Content-Length'] = 0
          
    
    
    return response

from django.contrib.auth import views as auth_views
def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            #request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
            request.session.set_expiry(0)
            
    return auth_views.login(request, *args, **kwargs)
