# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse
from .models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    mime_type = 'application/xml'
    """
    Create a type of RSS feed that has content:encoded elements.
    """

    # 修改channel标签的属性
    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    # 添加给个item标签下的其他元素的标签
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])

    # 添加自定义根标签
    def add_root_elements(self, handler):
        super(ExtendedRSSFeed, self).add_root_elements(handler)
        handler.addQuickElement('reporter', 'LL')


class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed   # 可不指定这个属性，默认是Rss201rev2Feed类型，可修改该参数，指定其他类型
    title = 'BlogPro'
    link = '/rss/'
    description = 'BlogPro is designed by django made by LL'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])

    def item_content_html(self, item):
        return item.content_html

    def item_author_name(self, item):
        return item.owner.username

    def item_author_email(self, item):
        return item.owner.email

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}






