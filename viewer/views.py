# Create your views here.
from django.template import RequestContext, loader 
from django.template.response import SimpleTemplateResponse
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


from lib.web import AjaxResponseContent, AjaxResponseContentSimple
from lib.imagesFromZip import imagesFromZip

from admin.models import Image,Gallery,Category,Comment,CommentForm

def pages(request,page):
    return(SimpleTemplateResponse('pages/%s.html' % page, RequestContext(request,{})))

def ajaxAddComment(request,cat=None,name=None):
    c = RequestContext(request)
    if request.method == 'POST':
        category=Category.objects.get(name=cat)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.gallery =  Gallery.objects.get(title=name)
            comment.author = form.cleaned_data['author']
            comment.title = form.cleaned_data['title']
            comment.content = form.cleaned_data['content']
            comment.email = form.cleaned_data['email']
            comment.save()
            return(SimpleTemplateResponse('viewer/ajax_comment_ok.html',c))
    else:
        form = CommentForm()
    c['comment_form'] = form
    c.update(csrf(request))
    return(SimpleTemplateResponse('viewer/ajax_comment_form.html',c))


def ajaxShowComment(request,cat=None,name=None):
    c = RequestContext(request)
    try:
        c['comments'] = Comment.objects.all().filter(gallery=Gallery.objects.get(title=name))
    except:
        pass
    return(SimpleTemplateResponse('viewer/ajax_comments.html',c))

def index(request,cat='',name=''):
    c = RequestContext(request)
    if name: 
        gallery = Gallery.objects.get(title=name)
        c['gallery'] = gallery
        c['images']  = Image.objects.all().filter(gallery=gallery)
        c['comments'] = Comment.objects.all().filter(gallery=gallery)
        c['comment_form'] = CommentForm()
        return(SimpleTemplateResponse('viewer/gallery.html',c))
    elif cat:
        category = Category.objects.get(name=cat)
        galleries = []
        for gallery in Gallery.objects.all().filter(category=category.id).order_by('created'):
            temp = {}
            temp['cover'] = Image.objects.all().filter(gallery=gallery.id)[0]
            temp['gallery'] = gallery
            galleries.append(temp)
        c = RequestContext(request)
        c['category'] = category
        c['galleries'] = galleries
        return(SimpleTemplateResponse('viewer/category.html',c))

    else:
        categories = []
        categories_temp = Category.objects.all()
        for category in categories_temp:
            temp = {}
            try:
                gallery = Gallery.objects.all().filter(category=category.id).order_by('created')[0]
                temp['cover'] = Image.objects.all().filter(gallery=gallery.id)[0]
            except:
                temp['cover'] = None

            temp['category'] = category
            temp['nb_gals'] = Gallery.objects.all().filter(category=category.id).count()
            categories.append(temp)

        c = RequestContext(request)
        c['categories'] = categories
        return(SimpleTemplateResponse('viewer/index.html',c))

        
