# -*- coding: utf-8 -*-

import json
from leon_base.base.views import BaseView, BaseParamsValidatorMixin


class ShopCatalogParamsValidatorMixin(BaseParamsValidatorMixin):

    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _ajax_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _grid_validator(value, default):
        return int(value) if value and int(value) else default

    @staticmethod
    def _grid_cnt_validator(value, default):
        return default

    @staticmethod
    def _order_validator(value, default):
        if value:
            return value
        else:
            return default

    @staticmethod
    def _page_validator(value, default):
        if value:
            return value
        else:
            return default

    @staticmethod
    def _filter_validator(value, default):
        try:
            return json.loads(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _product_validator(value, default):
        try:
            return json.loads(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _product_stock_validator(value, default):
        return value

    @staticmethod
    def _item_s_validator(value, default):
        return value

    @staticmethod
    def _cart_validator(value, default):
        return value

    @staticmethod
    def _count_validator(value, default):
        if value:
            return value
        else:
            return default

    @staticmethod
    def _catalog_slug_title_validator(value, default):
        return value

    @staticmethod
    def _product_slug_title_validator(value, default):
        return value


class ShopCatalogBaseView(BaseView):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    pass
