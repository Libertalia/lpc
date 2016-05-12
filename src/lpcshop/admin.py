# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableAdminMixin
from shop.admin.product import CMSPageAsCategoryMixin, ProductImageInline
from lpcshop.models import Bottle


@admin.register(Bottle)
class BottleAdmin(SortableAdminMixin, CMSPageAsCategoryMixin, admin.ModelAdmin):
    inlines = (ProductImageInline,)
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'unit_price', 'active',)
    search_fields = ('product_name',)
