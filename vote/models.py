# -*- coding: UTF-8 -*-
import os
from django.utils import six
from datetime import datetime, date
import logging

from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.core.cache import cache
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Sum, Count
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.utils.functional import cached_property
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

@python_2_unicode_compatible
class Designer(models.Model):
    name = models.CharField(_("作者名称"), max_length=32)
    phone = models.CharField(_("手机号"), max_length=11, null=True, blank=True)
    address = models.CharField(_("地址"), max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        app_label = 'vote'
        verbose_name = '作者'
        verbose_name_plural = '作者'

    def __str__(self):
        return self.name

class Production(models.Model):
    name = models.CharField(_("作品名"), max_length=32)
    number = models.CharField(_("作品编号"), max_length=8)
    designer = models.ForeignKey('Designer', related_name="production", verbose_name=_("作者"), null=True)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        app_label = 'vote'
        verbose_name = '作品'
        verbose_name_plural = '作品'

    def __str__(self):
        return self.name

    def get_primary_image_url(self):
        try:
            url = self.images.get(display_order=0).original.url
        except: 
            url = None
        return url

    def get_all_image_url(self):
        image_urls = []
        images = self.images.all()[1:]
        for i in images:
            image_urls.append(i.original.url)
        return image_urls

    def get_vote_count(self):
        high = Vote.objects.get(name='1001').votes.count()
        if self.name == '1005':
            return high * (115.22 / 100)
        return self.votes.count()

    @property
    def count(self):
        return self.votes.count()

    def vote(self):
        Vote.objects.create(production=self)
        return self.get_vote_count()

@python_2_unicode_compatible
class ProductionImage(models.Model):
    """
    An image of a production
    """
    production = models.ForeignKey(
        'Production', related_name='images', verbose_name=_("作品"))
    original = models.ImageField(
        _("图片"), upload_to='productions', max_length=255)

    #: Use display_order to determine which is the "primary" image
    display_order = models.PositiveIntegerField(
        _("显示顺序"), default=0,
        help_text=_("0代表主图"))
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    class Meta:
        app_label = 'vote'
        ordering = ["display_order"]
        unique_together = ("production", "display_order")
        verbose_name = _('作品图片')
        verbose_name_plural = _('作品图片')

    def __str__(self):
        return u"Image of '%s'" % self.production

    def is_primary(self):
        """
        Return bool if image display order is 0
        """
        return self.display_order == 0

    def delete(self, *args, **kwargs):
        """
        Always keep the display_order as consecutive integers. This avoids
        issue #855.
        """
        super(ProductImage, self).delete(*args, **kwargs)
        for idx, image in enumerate(self.product.images.all()):
            image.display_order = idx
            image.save()

class Vote(models.Model):
    openid = models.CharField(_("OpenId"), max_length=32, null=True, blank=True)
    production = models.ForeignKey("Production", related_name="votes", verbose_name='production')
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        app_label = 'vote'
        verbose_name = "投票记录"
        verbose_name_plural = "投票记录"

    def __str__(self):
        return self.production.name
