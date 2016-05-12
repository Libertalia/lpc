# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import serializers
from rest_framework.fields import empty
from shop.rest.serializers import (ProductSummarySerializerBase, ProductDetailSerializerBase,
    AddToCartSerializer)

Product = import_string('lpcshop.models.bottles.Bottle')


class ProductSummarySerializer(ProductSummarySerializerBase):
    media = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_url', 'product_type', 'product_model', 'price',
                  'media',)

    def get_media(self, product):
        return self.render_html(product, 'media')


class ProductDetailSerializer(ProductDetailSerializerBase):
    class Meta:
        model = Product
        exclude = ('active',)


class AddSmartCardToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles SmartCards
    """
    def get_instance(self, context, data, extra_args):
        product = context['product']
        extra = context['request'].data.get('extra', {})
        extra.setdefault('product_code', product.product_code)
        instance = {
            'product': product.id,
            'unit_price': product.unit_price,
            'extra': extra,
        }
        return instance


class AddBottleToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles Bottles
    """
    def get_instance(self, context, data, extra_args):
        product = context['product']
        extra = data['extra'] if data is not empty else {}
        try:
            variant = product.get_product_variant(extra.get('product_code'))
        except product.DoesNotExist:
            variant = product.smartphone_set.first()
        instance = {
            'product': product.id,
            'unit_price': variant.unit_price,
            'extra': {'product_code': variant.product_code}
        }
        return instance
