
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


# ================================================================================
# OLD APPROACHES
# ================================================================================

# # Function-based view (original)
# urlpatterns = [
#     path('products/', views.product_list),
#     path('products/<int:id>/', views.product_detail),
# ]

# # Class-based view without mixins
# urlpatterns = [
#     path('products/', views.product_list),
#     path('products/<int:id>/', views.ProductDetailsView.as_view()),
# ]

# # Mixin-based views
# urlpatterns = [
#     path('products/', views.ProductListView.as_view()),
#     path('products/<int:pk>/', views.ProductDetailView.as_view()),
# ]


# ================================================================================
# ROUTER FOR VIEWSETS
# ================================================================================
# Routers automatically generate URL patterns for ViewSets
#
# What DefaultRouter creates:
# ---------------------------
# GET    /products/          → ProductViewSet.list()
# POST   /products/          → ProductViewSet.create()
# GET    /products/{id}/     → ProductViewSet.retrieve()
# PUT    /products/{id}/     → ProductViewSet.update()
# PATCH  /products/{id}/     → ProductViewSet.partial_update()
# DELETE /products/{id}/     → ProductViewSet.destroy()
#
# Plus custom actions:
# GET    /products/recent/       → ProductViewSet.recent()
# POST   /products/{id}/discount/ → ProductViewSet.discount()
#
# Router also generates a root API view at: /products/ (with format suffixes)

# router = DefaultRouter()

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('carts', views.CartViewSet, basename='cart')


product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet,
                        basename='product-reviews')
# Create nested router for cart items (similar to product reviews)
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

# The router.urls contains all auto-generated URL patterns
urlpatterns = router.urls + product_router.urls + cart_router.urls

# Alternative: If you want to mix manual URLs with router URLs:
# urlpatterns = [
#     path('', include(router.urls)),  # Include router URLs
#     path('custom/', views.custom_view),  # Add manual URLs
# ]
