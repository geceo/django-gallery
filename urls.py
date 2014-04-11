from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from gallery.lib.web import LatestGalleryFeed

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gallery/', include('gallery.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', redirect_to, {'url': '/gallery'}),
    (r'^login$', 'gallery.admin.views.uLogin'),
    (r'^logout$', 'gallery.admin.views.uLogout'),
    (r'^admin/$', 'gallery.admin.views.index'),

    (r'^admin/general/$', 'gallery.admin.views.generalSettings'),
    (r'^admin/addGallery/$', 'gallery.admin.views.addGallery'),
    (r'^admin/editGallery/(?P<id>.*)/$', 'gallery.admin.views.editGallery'),
    (r'^admin/deleteGallery/(?P<id>.*)/$', 'gallery.admin.views.deleteGallery'),

    (r'^admin/addCategory$', 'gallery.admin.views.addCategory'),
    (r'^admin/deleteCategory/(?P<id>.*)/$', 'gallery.admin.views.deleteCategory'),
    (r'^admin/editCategory/(?P<id>.*)/$', 'gallery.admin.views.editCategory'),

    (r'^gallery/$', 'gallery.viewer.views.index'),
    (r'^gallery/(?P<cat>.*)/(?P<name>.*)/$', 'gallery.viewer.views.index'),
    (r'^gallery/(?P<cat>.*)/$', 'gallery.viewer.views.index'),
    (r'^(?P<page>(about|buy))/', 'gallery.viewer.views.pages'),
    (r'^gallery/(?P<cat>.*)/(?P<name>.*)/ajaxAddComment$', 'gallery.viewer.views.ajaxAddComment'),
    (r'^gallery/(?P<cat>.*)/(?P<name>.*)/ajaxShowComment$', 'gallery.viewer.views.ajaxShowComment'),
    (r'^(latest|feed)/$',LatestGalleryFeed()),

    #(r'^accounts/admin$', 'gallery.accounts.views.admin'),

    (r'^datas/(?P<path>.*)$' , 'django.views.static.serve' , { 'document_root': '/root/Ospow-Django-Gallery/gallery/datas/' })
)
