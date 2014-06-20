# Create your views here.
from django.template import RequestContext, loader
from django.template.response import SimpleTemplateResponse

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.forms.models import modelformset_factory


from django.utils import simplejson

from lib.web import AjaxResponseContent, AjaxResponseContentSimple
from lib.imagesFromZip import imagesFromZip

from general.models import Settings, SettingsForm

from tempfile import NamedTemporaryFile
from PIL import Image as PILImage
from math import sqrt
import StringIO
import re 

from admin.models import Image,ImageForm,Gallery,GalleryForm,Category,CategoryForm,UploadForm,LoginForm

from django.contrib.auth import authenticate, login, logout

def uLogin(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                return(HttpResponseRedirect('/admin/'))
    c = RequestContext(request,csrf(request))
    c['form'] = form
    return(SimpleTemplateResponse('admin/login.html',c))

def uLogout(request):
    logout(request)
    return(HttpResponseRedirect('/'))

            
@login_required
def generalSettings(request):
    if request.method == 'POST':
        coin()
        form = SettingsForm(instance=request.POST)
        form.save()
        return(HttpResponseRedirect('/admin/'))
    return(HttpResponseRedirect('/admin/'))

@login_required
def index(request):
    c = RequestContext(request,{
        'form': SettingsForm(),
        'galleries': Gallery.objects.all(),
        'categories': Category.objects.all()
    })
    return(SimpleTemplateResponse('admin/index.html',c))

def addGallery(request):
    if request.method == 'GET':
        form = UploadForm()
        c  = RequestContext(request, {
        'form' : form
        })
        c.update(csrf(request))
        return(SimpleTemplateResponse('admin/upload.html', c))
    else:
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            # First, copy zipfile to a tmpfile
            zipfile = NamedTemporaryFile(delete=False)
            zipfile.write(request.FILES['file'].read())
            zipfile.close()
            # Now we got the Zip, unzip it!!
            imagesObj = imagesFromZip(zipfile.name)
            imagesList = imagesObj.listImages()
            # Is there images in this zip ?
            if len(imagesList) > 0:
                # regexp for extractiong name ...
                nameRe = re.compile('/([^/]+)$')
                # Create corresponding gallery
                gallery = Gallery()
                gallery.title = form.cleaned_data['title']
                gallery.desc  = form.cleaned_data['desc']
                gallery.category = form.cleaned_data['category']
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
                    new_s = 1024*768
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
                return(HttpResponseRedirect(reverse('gallery.admin.views.editGallery',kwargs={'id': gallery.pk})))
            # Cleanup...
            imagesObj.cleanup()
            os.rm(zipfile)
        else:
            c = RequestContext(request,csrf(request))
            c['form'] = form
            return(SimpleTemplateResponse('admin/upload.html', c))

		
def editGallery(request,id):
    ImagesFS = modelformset_factory(Image, fields=('name','description',))
    # Initial forms 
    gallery = None
    imagesForm = None
    images = Image.objects.filter(gallery=id)
    
    if request.method == 'POST':
        if 'editGal' in request.POST:
            # First, try to get gallery form
            gallery = GalleryForm(request.POST,instance=Gallery.objects.get(pk=id))
            if gallery.is_valid():
                gallery.save()
        elif 'editImg' in request.POST:
            # Then, the formset
            imagesForm = ImagesFS(request.POST)
            imagesForm.save()

    # First, build gallery form
    gallery = GalleryForm(instance=Gallery.objects.get(pk=id))
    # Then build a formset for images
    imagesForm = ImagesFS(queryset=Image.objects.filter(gallery=id))
    c = RequestContext(request,csrf(request))
    c.update({
        'gallery': gallery,
        'images': images,
        'imagesForm': imagesForm,
        'mixed': zip(images,imagesForm.forms)
    })
    return(SimpleTemplateResponse('admin/editGallery.html',c))

def deleteGallery(request,id):
    gallery = Gallery.objects.all().get(pk=id)
    images  = Image.objects.all().filter(gallery=id)        
    for image in images:
        image.delete()
    gallery.delete()
    return(HttpResponseRedirect('/admin/'))

def addCategory(request):
    if request.method == 'GET':
        form = CategoryForm()
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return(HttpResponseRedirect('/admin/'));
    c = RequestContext(request, { 'form': form})
    c.update(csrf(request))
    return(SimpleTemplateResponse('admin/addCategory.html',c))
        

def editCategory(request,id):
    if request.method == 'GET':
        form = CategoryForm(instance=Category.objects.get(pk=id))
    elif request.method == 'POST':
        form = CategoryForm(request.POST,instance=Category.objects.get(pk=id))
        if form.is_valid():
            form.save()
            return(HttpResponseRedirect('/admin/'));
    c = RequestContext(request, { 'form': form})
    c.update(csrf(request))
    return(SimpleTemplateResponse('admin/editCategory.html',c))

def deleteCategory(request,id):
    category = Category.objects.all().get(pk=id)
    category.delete()
    return(HttpResponseRedirect('/admin/'))
