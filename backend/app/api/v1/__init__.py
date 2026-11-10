from .endpoints.products import router as router_product
from .endpoints.user import router as router_user
from .endpoints.category import router as router_category
from .endpoints.cart import router as router_cart
from .endpoints.favorite import router as router_favorite
from .endpoints.review import router as router_review
from .endpoints.order import router as router_order
from .endpoints.address import router as router_address
from .endpoints.promotion import router as router_promotion
from .endpoints.auth import router as router_auth


__all__ = ['router_product',
           'router_user',
           'router_category',
           'router_cart',
           'router_favorite',
           'router_review',
           'router_order',
           'router_address',
           'router_promotion',
           'router_auth']