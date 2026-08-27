from .endpoints.products import router as router_product
from .endpoints.user import router as router_user
from .endpoints.category import router as router_category
from .endpoints.cart import router as router_cart
from .endpoints.favorite import router as router_favorite

__all__ = ['router_product','router_user','router_category','router_cart','router_favorite']