from __future__ import unicode_literals

from django.conf import settings

# import default models from djangoSHOP to materialize them
from shop.models.defaults.address import ShippingAddress, BillingAddress
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.defaults.customer import Customer
from shop.models.defaults.order import Order
from shop.models.defaults.order_item import OrderItem

from .bottles import Bottle
