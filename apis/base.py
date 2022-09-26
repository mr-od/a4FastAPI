from fastapi import APIRouter

from apis.version1 import route_general_pages
# from apis.version1 import route_login
from apis.version1 import route_products
from apis.version1 import route_vendors
# from apis.version1 import route_search
from apis.version1 import route_users
from apis.version1 import route_orders


api_router = APIRouter()

api_router.include_router(
    route_general_pages.general_pages_router, prefix="", tags=["General_Pages"])

# api_router.include_router(route_login.router,
#                           prefix="/auth", tags=["Login"])

api_router.include_router(route_vendors.vendors_routers,
                          prefix="/vendors", tags=["Vendors"])

api_router.include_router(route_products.products_routers,
                          prefix="/products", tags=["Products"])

# api_router.include_router(route_search.router,

#                           prefix="/search", tags=["Search"])

api_router.include_router(route_users.users_routers,

                          prefix="/users", tags=["Users Route"])

api_router.include_router(route_orders.orders_routers,

                          prefix="/orders", tags=["Orders Route"])
