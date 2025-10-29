from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Count

from store.models import Product, Customer, Collection, Order

# Register your models here.


# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name',
#                     'email', 'phone', 'membership')


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'price', 'inventory', 'collection')


# class CollectionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'featured_product')
#     search_fields = ['title']


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'placed_at', 'customer')


# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Collection, CollectionAdmin)
# admin.site.register(Order, OrderAdmin)


# using decorator syntax
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'email', 'phone', 'membership')
    list_editable = ['phone']
    list_per_page = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'inventory',
                    'inventory_status', 'collection')

    list_select_related = ['collection']
#   Without list_select_related:
#   - Query 1: Fetch all products (e.g., 100 products)
#   - Query 2-101: For each product, fetch its collection (100 additional
#   queries)
#   - Total: 101 queries

#      ✅ Use for:
#   - ForeignKey fields displayed in list_display
#   - OneToOneField fields
#   - Fields accessed in custom methods that display in the list view

#   ❌ Don't use for:
#   - ManyToManyField (use list_prefetch_related instead)
#   - Reverse ForeignKey relationships (use prefetch_related)

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 60:
            return 'Low'
        return 'OK'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'featured_product', 'product_count')
    search_fields = ['title']  # Adding search functionality by title
    # list_editable = ['featured_product']

    @admin.display(ordering='products_count')
    def product_count(self, collection):

        return collection.products_count

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

    # annotate is a aggregation function that adds a calculated field to each
    # object in the queryset. In this case, it adds products_count which counts


#    Without annotate:
#   collections = Collection.objects.all()
#   for collection in collections:
#       # To get product count, you'd need a separate query
#       count = collection.products.count()  # ❌ Separate query for EACH
#   collection!

#   With annotate:
#   collections = Collection.objects.annotate(
#       products_count=Count('products')
#   )
#   for collection in collections:
#       # Count is already available!
#       count = collection.products_count  # ✅ No extra query!


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'placed_at', 'customer')
