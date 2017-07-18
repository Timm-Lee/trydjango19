# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.

def upload_location(instance, filename):
    extension = filename.split(".")[-1]
    return "{0}/{0}.{1}".format(instance.id, extension)


class Post(models.Model):
    # title = models.CharField(max_length=150, verbose_name=u'标题')
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    # return "/posts/{0}".format(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]
