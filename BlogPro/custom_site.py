# -*- coding: utf-8 -*-

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'BlogPro'
    site_title = 'BlogPro管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
