# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: uploadfile.py
# Creation Date: 2011-11-04  16:37
# Last Modified: 2011-11-12 18:40:4
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
import os,datetime,random
#import urllib
# ------------------------------------------------------------

# django.

from django.conf import settings
# ------------------------------------------------------------

# 3dpart.
#
# ------------------------------------------------------------

# ddtcms.
#from models import MODEL
#from forms  import AForm,BForm
# ------------------------------------------------------------

# config.
#FIELD_MAX_LENGTH = getattr(settings, 'FIELD_MAX_LENGTH', 100)
#n_dict={
#"sitename":"Example",
#}
# ------------------------------------------------------------


def genfilename(filext):
	randomfilename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randrange(0, 100, 2)).rjust(2,'0') + random.choice('abcdefghijklmnopqrstuvwxyz')
	randomfilename ="%s%s" % (randomfilename , filext)
	return randomfilename

def randomfilename(filename):
	if len(filename)>0:
		base, ext = os.path.splitext(filename)
		ran_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randrange(0, 100, 2)).rjust(2,'0') + random.choice('abcdefghijklmnopqrstuvwxyz')
		ran_filename = "%s%s" % (ran_filename , ext)
		return ran_filename
	else:
		return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randrange(0, 100, 2)).rjust(2,'0') +".tmp"

def handle_uploaded_file(f):
    UPLOAD_TO = 'files/%s/' % (datetime.datetime.now().strftime('%Y/%m/%d'))
    SAVE_TO   = os.path.join(settings.MEDIA_ROOT,UPLOAD_TO)

    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO)

    try:
        fileext=os.path.splitext(f.name)[1]
    except:
        fileext='.tmp'

    filename     = genfilename(fileext)
    upfilename   = os.path.join(UPLOAD_TO,filename)
    diskfilename = os.path.join(SAVE_TO,filename)

    destination = open(diskfilename, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    #try:
    #    im = PIL.Image.open(filename)
    #    im=im.convert('RGB')
    #    name = settings.STATIC_UPLOAD+'face/u%s.png' % (datetime.datetime.now().strftime('%Y-%m-%d'))
    #    im.save(file(name, 'wb'), 'PNG')
    #except:
    #    return "ERROR"

    return upfilename,diskfilename