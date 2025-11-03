
from django.contrib import admin
from django.urls import include, path
from playground import views


admin.site.site_header = 'Storefront Admin'
admin.site.site_title = 'Storefront Admin Portal'
admin.site.index_title = 'Welcome to the Storefront Admin'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', views.say_hello),
    path('playground/q/', views.q_objects_demo),
    path('playground/f/', views.f_objects_demo),
    path('playground/lookups/', views.field_lookups_demo),
    path('playground/aggregation/', views.aggregation_methods_demo),
    path('playground/annotate/', views.annotate_values_demo),
    path('playground/select-prefetch/', views.select_prefetch_demo),
    path('playground/crud/', views.crud_operations_demo),
    path('playground/transactions/', views.transactions_demo),



    # store
    path('store/', include('store.urls')),
]
