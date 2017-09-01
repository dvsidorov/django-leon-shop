# coding: utf-8


import datetime
from . import models


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class DiscountMixin(object):

    pass


class Basket(object):

    """ Class for operate cart in session.
        Using request.session dict, where
        find CART_ID and if cart object
        not expired and find, return it,
        else, create new object cart.
    """

    BASKET_MODEL = None
    ITEM_MODEL = None

    def __init__(self, basket_id):
        if basket_id:
            try:
                basket = self.BASKET_MODEL.objects.get(id=basket_id, checked_out=False)
                self.id = basket.id
            except self.BASKET_MODEL.DoesNotExist:
                basket = self.new()
        else:
            basket = self.new()
        self.basket = basket
        self.price = 0

    def __iter__(self):
        for item in self.basket.item_set.all():
            yield item

    def new(self):
        basket = self.BASKET_MODEL(creation_date=datetime.datetime.now())
        basket.save()
        self.id = basket.id
        return basket

    def get_image(self, product):
        return product.small_image \
               or product.big_image \
               or product.super_big_image

    def add(self, product, quantity=1):
        item_s = self.ITEM_MODEL.objects.filter(cart=self.id,
                                                product=product).all()

        if item_s:
            item = item_s[0]
            item.quantity += int(quantity)
        else:

            item = models.Item(cart=self.basket,
                               product=product,
                               quantity=quantity,
                               image=self.get_image(product))

        item.save()

    def remove(self, product, ):
        item_s = self.ITEM_MODEL.objects.filter(cart=self.id,
                                                product=product).all()
        if item_s:
            item = item_s[0]
            item.delete()
        else:
            raise ItemDoesNotExist

    def update(self, product, quantity=1, print_type=None):
        item_s = self.ITEM_MODEL.objects.filter(cart=self.id,
                                                product=product).all()
        if item_s:
            item = item_s[0]
        else:
            item = self.ITEM_MODEL(cart=self.id,
                                   product=product,
                                   quantity=quantity,
                                   image=self.get_image(product))
        item.quantity = quantity
        item.save()

    def calculate(self):
        total_price = 0
        for item in self.basket.item_set.all():
            item.unit_price = item.product.price
            item.item_price = item.unit_price * item.quantity
            item.save()
            total_price += item.item_price
        self.price = total_price

    def clear(self):
        for item in self.basket.item_set.all():
            item.delete()

    def get_quantity(self, product):
        item_s = self.ITEM_MODEL.objects.filter(cart=self.id,
                                                product=product).all()
        if item_s:
            item = item_s[0]
            return item.quantity
        else:
            raise ItemDoesNotExist

    def checkout_cart(self):
        self.basket.checked_out = True
        self.basket.save()
        return True

    def total(self):
        total = 0
        for item in self.basket.item_set.all():
            total += item.total_price
        return total

    def item_count(self):
        total = 0
        for item in self.basket.item_set.all():
            total += item.quantity
        return total

    def has_items(self):
        return self.item_count() > 0
