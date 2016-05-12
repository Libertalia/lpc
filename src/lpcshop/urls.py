# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from shop.views.catalog import AddToCartView, CMSPageProductListView, ProductRetrieveView
from lpcshop.serializers import (
    ProductSummarySerializer,
    ProductDetailSerializer,
)

urlpatterns = patterns('',
    url(r'^$', CMSPageProductListView.as_view(
        serializer_class=ProductSummarySerializer,
    )),
    url(r'^(?P<slug>[\w-]+)$', ProductRetrieveView.as_view(
        serializer_class=ProductDetailSerializer
    )),
    url(r'^(?P<slug>[\w-]+)/add-to-cart', AddToCartView.as_view()),
)
