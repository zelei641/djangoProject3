from django.db import models

# Create your models here.
class userUploadPhotos(models.Model):
    photosname = models.CharField(verbose_name='文件名称',max_length=256)
    photostate = models.CharField(verbose_name='处理状态', max_length=256)

class userGetPhotos(models.Model):
    photosname = models.CharField(verbose_name='文件名称',max_length=256)
    photostate = models.CharField(verbose_name='处理状态', max_length=256)