# coding=utf-8
from django.template.response import SimpleTemplateResponse
from django.utils.encoding import smart_unicode
from gallery.viewer.views import index as index_func
from general.models import Settings

class GalleryMiddleware():
    def __init__(self):
        self.general_title = 'Gérald Colangelo\'s Portfolio'
        self.page_address = None
        self.title = self.general_title

    def process_view(self,request,view_func,view_args,view_kwargs):
        self.page_address = u'http://portfolio.yanluo.net'+request.path
        self.navpath = [ ('/gallery/', self.general_title) ]
        
        tmp = '/'
        for pathelt in request.path.split('/')[1:-1]:
            tmp += pathelt+'/'
            self.navpath.append((tmp,pathelt))
	try:
		self.title = u'%s : %s' % ( smart_unicode(self.general_title) , smart_unicode(pathelt.capitalize()))
	except:
		self.title = smart_unicode(self.general_title)
        return None

    def process_template_response(self,request,response):
        if response.context_data:
            response.context_data['title'] = self.title
            response.context_data['navpath'] = self.navpath
            response.context_data['general_title'] = self.general_title
            response.context_data['page_address'] = self.page_address
        return(response)
        
        
