from django.db import models
from django import forms
from django.forms import ModelForm

# Create your models here.
class Settings(models.Model):
    # General gallery informations
    general_title = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    url   = models.CharField(max_length=255)

    # Facebook connector
    facebook_appid = models.CharField(blank=True,max_length=255)
    facebook_appsecret = models.CharField(blank=True,max_length=255)
    facebook_profile_id = models.CharField(blank=True,max_length=255)
    facebook_canvas_url =  models.CharField(blank=True,max_length=255)

    # Twitter connector
    twitter_account = models.CharField(max_length=255)
    twitter_consumer_key = models.CharField(max_length=255)
    twitter_consumer_secret = models.CharField(max_length=255)
    twitter_access_token = models.CharField(max_length=255)
    twitter_access_token_secret = models.CharField(max_length=255)

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
