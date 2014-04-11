# encoding=utf-8
from django.db import models
from django import forms
from django.forms import ModelForm

import PIL

# Create your models here.
class Gallery(models.Model):
    # Title and description
    title = models.CharField(max_length=255,unique=True,help_text='Titre de votre galerie',verbose_name='Titre')
    desc = models.TextField(blank=True,help_text='La description de votre gallerie',verbose_name='Description')
    category = models.ForeignKey('Category',help_text='Catégorie ou classer la galerie',verbose_name='Catégorie')
    # Datestamp
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    # Gallery votes
    u_vote = models.IntegerField(blank=True)
    d_vote = models.IntegerField(blank=True)
    # TODO:
    # user = models.ForeignKey('User')
    # published = models.BooleanField(blank=True)

    def __init__(self,*args, **kwargs):
        super(Gallery,self).__init__(*args, **kwargs)
        # Votes
        self.d_vote = 0
        self.u_vote = 0
    def __str__(self):
        return(self.title.encode('ascii','xmlcharrefreplace'))

class Comment(models.Model):
    # Title and description
    author = models.CharField(max_length=255,help_text='Votre pseudo, sera affiché',verbose_name='Pseudo')
    email = models.EmailField(max_length=255,help_text='Votre email, ne sera pas affiché',verbose_name='Email')
    url = models.URLField(max_length=255,blank=True,null=True,help_text='L\'adresse de votre page perso',verbose_name='Page perso')
    title = models.CharField(max_length=255,help_text='Titre de votre commentaire',verbose_name='Titre')
    content = models.TextField(blank=False,help_text='Votre commentaire',verbose_name='Commentaire')
    gallery  = models.ForeignKey('Gallery')
    # Datestamp
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    # Gallery votes
    u_vote = models.IntegerField(blank=True,null=True)
    d_vote = models.IntegerField(blank=True,null=True)
    approved = models.BooleanField(blank=True)
    # TODO:
    # user = models.ForeignKey('User')
    # published = models.BooleanField(blank=True)



class Image(models.Model):
    #name     = models.CharField(max_length=255,help_text='Nom de votre image, determine l\'ordre dans la gallerie (alphabétique)',verbose_name='Nom de l\'image')
    original = models.ImageField(upload_to='originals/%Y/%m/%d')
    screen   = models.ImageField(upload_to='screen/%Y/%m/%d')
    thumb    = models.ImageField(upload_to='thumb/%Y/%m/%d')
    gallery  = models.ForeignKey('Gallery')
    description = models.TextField(blank=True,help_text='Description de l\'image',verbose_name='Description')
    
class Category(models.Model):
    name = models.CharField(max_length=255,help_text='Nom de la galerie',verbose_name='Nom')
    description = models.TextField(help_text='Description de la galerie',verbose_name='Description')
    def __str__(self):
        return(self.name.encode('ascii','xmlcharrefreplace'))
	


class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        exclude = ('d_vote','u_vote')

class UploadForm(ModelForm):
    file = forms.FileField(required=True)
    class Meta:
        model = Gallery
        fields = ('title','desc','category',)

class CategoryForm(ModelForm):
    class Meta:
        model = Category

from django.forms.widgets import Widget
from django.utils.html import escape, conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class ImagePrintWidget(Widget):
    def __init__(self, attrs=None):
        default_attrs = { }
        if attrs:
            default_attrs.update(attrs)
        super(ImagePrintWidget,self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None: 
            value=''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<img %s src=%s/>' % (flatatt(final_attrs),force_unicode(value)))

class ImageForm(ModelForm):
    thumbnail = ImagePrintWidget()
    rotate = forms.BooleanField()
    class Meta:
        model = Image
        exclude = ('thumb','screen','original','gallery')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('u_vote','d_vote','approved','gallery')
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'input-small'
        self.fields['content'].widget.attrs['class'] = 'input-medium'
        self.fields['content'].widget.attrs['rows'] = '4'
        self.fields['content'].widget.attrs['cols'] = '40'
        self.fields['title'].widget.attrs['class'] = 'input-medium'
    
class LoginForm(forms.Form):
    username = forms.CharField(required=True,max_length=255,help_text='Your username')
    password = forms.CharField(required=True,max_length=244,help_text='Your password',
                                widget=forms.PasswordInput())
