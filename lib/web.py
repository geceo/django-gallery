# coding=utf-8
from django.utils import simplejson
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from django.contrib.syndication.views import Feed
from admin.models import Gallery, Image

from django.template.defaultfilters import escape


class LatestGalleryFeed(Feed):
    title = 'Portfolio'
    link  = 'http://portfolio.yanluo.net/gallery/'
    description = 'Urbex photography, street photography, instants and thoughts ...'

    def items(self):
        return Gallery.objects.order_by('-modified')[:10]

    def item_title(self,item):
        return item.title

    def item_description(self,item):
        img_count = Image.objects.filter(gallery=item.pk).count()
        thumb = Image.objects.filter(gallery=item.pk)[0].thumb
        return "<img style='float: left' src='%s%s'/><p><strong>%i photos in this gallery</strong><br>%s<br></div></p>" % ( 'http://portfolio.yanluo.net', thumb.url, img_count, item.desc[:100] )
    
    def item_link(self,item):
        return u'%s%s/%s/' % ( self.link, escape(item.category.name), escape(item.title) ) 

def AjaxResponseContent(request,template,context):
    http_response = render_to_response(template,context)
    output = simplejson.dumps({'content':http_response.content})
    return(HttpResponse(output))

def AjaxResponseContentSimple(request,status,back_url):
    context = { "back" : back_url, "status": status }
    http_response = render_to_response("common/simple_success_error.html",context)
    output = simplejson.dumps({'content':http_response.content})
    return(HttpResponse(output))
