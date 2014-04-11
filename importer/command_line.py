from images.models import Image,Gallery
from django.core.files.base import ContentFile


from lib.imagesFromZip import imagesFromZip

from tempfile import NamedTemporaryFile
from PIL import Image as PILImage
from math import sqrt
import sys
import StringIO
import re


def importZip(zipfile,galleryName,galleryDescription):
    # Stuff bgins here ...
    imagesObj = imagesFromZip(zipfile)
    imagesList = imagesObj.listImages()
    # Is there images in this zip ?
    if len(imagesList) > 0:
        # regexp for extractiong name ...
        nameRe = re.compile('/([^/]+)$')
        # Create corresponding gallery
        gallery = Gallery()
        gallery.title = galleryName
        gallery.desc  = galleryDescription
        gallery.save() # Must save gallery 
        # Now, for each images in it, create an image object and bind it to gallery
        for imgPath in imagesList:
            src = PILImage.open(imgPath)
            m = nameRe.search(imgPath)
            imgObj = Image()
            imgObj.gallery = gallery
            # First, put the original sized picture
            # use StringIO hack to save image to a string ...
            output = StringIO.StringIO()
            src.save(output,'JPEG')
            imgObj.original.save(m.groups()[0],ContentFile(output.getvalue()))
            output.close()
            # Then, resize it to something like 1600*1200
            (orig_w,orig_h) = src.size
            orig_s = orig_w * orig_h
            new_s = 1600*1200
            ratio = orig_s/new_s
            # Resize only if requested size is lower than original
            if ratio > 1:
                (new_w, new_h) = ( orig_w/(sqrt(ratio)),orig_h/(sqrt(ratio)) )
                resized = src.resize((int(new_w),int(new_h)))
            else: # Else, just keep original one ...
                (new_w, new_h) = (orig_w, orig_h)
                resized = src
            output = StringIO.StringIO()
            resized.save(output,'JPEG')
            imgObj.screen.save(m.groups()[0],ContentFile(output.getvalue()))
            output.close()
            # Finally, get a thumb of 150px*150px, work on resized picture to be faster
            if new_w < new_h:
                maxi = new_w
            else:
                maxi = new_h
            thumb = resized.transform((150,150),PILImage.EXTENT,(0,0,maxi,maxi))
            output = StringIO.StringIO()
            thumb.save(output,'JPEG')
            imgObj.thumb.save(m.groups()[0],ContentFile(output.getvalue()))
            output.close()
            imgObj.save()
        gallery.save()
        print "done !"
