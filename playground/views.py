from django.shortcuts import render
from django.http import HttpResponse
from django.db import models, transaction
from django.db.models import Q, F, Count, Sum, Avg, Max, Min, Value, DecimalField, ExpressionWrapper
from django.db.models.functions import Concat
from decimal import Decimal
from store.models import Product, Customer, Collection, Order

# Create your views here.


#   ExpressionWrapper tells Django what type of data a complex expression will return .

#   The Problem:

#   When you do calculations with different field types, Django can't always figure out what
#   type the result should be:

#   # This causes an error:
#   Product.objects.annotate(
#       total_value=F('price') * F('inventory')  # DecimalField * IntegerField = ???
#   )
#   # Error: Cannot infer type of '*' expression

#   The Solution:

#   ExpressionWrapper wraps your expression and specifies the output type:

#   # This works:
#   Product.objects.annotate(
#       total_value=ExpressionWrapper(
#           F('price') * F('inventory'),
#           output_field=DecimalField()  # Tell Django the result is a Decimal
#       )
#   )

#   Syntax:

#   ExpressionWrapper(
#       expression,           # Your calculation (F('field') * 10, etc.)
#       output_field=Type()   # The data type of the result
#   )


def say_hello(request):
    # ============================================
    # STEP 1: GET ALL OBJECTS
    # ============================================
    # Get all products from database
    all_products = Product.objects.all()

    # Get all customers from database
    all_customers = Customer.objects.all()

    # ============================================
    # STEP 2: FILTER - Get specific records
    # ============================================
    # Get products with price greater than 100
    expensive_products = Product.objects.filter(price__gt=100)

    # Get products with price less than or equal to 50
    cheap_products = Product.objects.filter(price__lte=50)

    # Get customers with Gold membership
    gold_customers = Customer.objects.filter(membership='G')

    # Get customers with Bronze membership
    bronze_customers = Customer.objects.filter(membership='B')

    # ============================================
    # STEP 3: GET - Get single object by ID
    # ============================================
    # Get product with ID = 1
    # product = Product.objects.get(id=1)

    # Get customer with ID = 1
    # customer = Customer.objects.get(id=1)

    # ============================================
    # STEP 4: EXCLUDE - Get all except condition
    # ============================================
    # Get all customers EXCEPT Gold members
    non_gold_customers = Customer.objects.exclude(membership='G')

    # Get all products EXCEPT those with inventory below 10
    well_stocked_products = Product.objects.exclude(inventory__lt=10)

    # ============================================
    # STEP 5: ORDERING - Sort results
    # ============================================
    # Get products ordered by price (ascending)
    products_by_price_asc = Product.objects.all().order_by('price')

    # Get products ordered by price (descending)
    products_by_price_desc = Product.objects.all().order_by('-price')

    # Get customers ordered by first name
    customers_by_name = Customer.objects.all().order_by('first_name')

    # ============================================
    # STEP 6: LIMITING RESULTS - Get first few
    # ============================================
    # Get first 5 products
    first_5_products = Product.objects.all()[:5]

    # Get first 3 customers
    first_3_customers = Customer.objects.all()[:3]

    # ============================================
    # STEP 7: CHAINING - Combine multiple queries
    # ============================================
    # Get Gold customers ordered by first name
    gold_customers_sorted = Customer.objects.filter(
        membership='G').order_by('first_name')

    # Get expensive products with low inventory, sorted by price
    critical_products = Product.objects.filter(
        price__gt=100, inventory__lt=20).order_by('-price')

    # ============================================
    # STEP 8: COUNT - Count matching records
    # ============================================
    # Count total products
    total_products = Product.objects.count()

    # Count Gold customers
    gold_count = Customer.objects.filter(membership='G').count()

    # ============================================
    # STEP 9: EXISTS - Check if records exist
    # ============================================
    # Check if any products exist
    has_products = Product.objects.exists()

    # Check if any Gold customers exist
    has_gold_customers = Customer.objects.filter(membership='G').exists()

    # ============================================
    # OUTPUT: Display results
    # ============================================
    # Print query results to response
    return HttpResponse(f"""
        <h1>Django Query Examples</h1>

        <h2>Step 1: Get All</h2>
        <p>Total Products: {all_products.count()}</p>
        <p>Total Customers: {all_customers.count()}</p>

        <h2>Step 2: Filter</h2>
        <p>Expensive Products (>100): {expensive_products.count()}</p>
        <p>Gold Customers: {gold_customers.count()}</p>

        <h2>Step 5: Ordering</h2>
        <p>First product by price: {products_by_price_asc.first()}</p>

        <h2>Step 8: Count</h2>
        <p>Total Products: {total_products}</p>
        <p>Gold Members: {gold_count}</p>
    """)


def q_objects_demo(request):
    """
    Demonstrates Q objects for complex queries with OR and AND operators.
    Q objects allow you to combine multiple conditions using | (OR) and & (AND).
    """

    # ============================================
    # STEP 1: OR QUERIES - Match ANY condition
    # ============================================
    # Get products that are EITHER cheap (<=50) OR expensive (>100)
    cheap_or_expensive = Product.objects.filter(
        Q(price__lte=50) | Q(price__gt=100))

    # Get customers who are EITHER Gold OR Silver members
    gold_or_silver = Customer.objects.filter(
        Q(membership='G') | Q(membership='S'))

    # ============================================
    # STEP 2: AND QUERIES - Match ALL conditions
    # ============================================
    # Get products that are BOTH expensive AND low in stock
    expensive_and_low_stock = Product.objects.filter(
        Q(price__gt=100) & Q(inventory__lt=20))

    # ============================================
    # STEP 3: COMBINING OR and AND
    # ============================================
    # Get products that are (cheap AND low stock) OR (expensive AND high stock)
    complex_query = Product.objects.filter(
        (Q(price__lte=50) & Q(inventory__lt=10)) |
        (Q(price__gt=100) & Q(inventory__gt=50))
    )

    # ============================================
    # STEP 4: NOT QUERIES - Negate conditions with ~
    # ============================================
    # Get products that are NOT cheap (opposite of price <= 50)
    not_cheap = Product.objects.filter(~Q(price__lte=50))

    # Get customers who are NOT Gold members
    not_gold = Customer.objects.filter(~Q(membership='G'))

    # Get products that are expensive BUT NOT low in stock
    expensive_not_low_stock = Product.objects.filter(
        Q(price__gt=100) & ~Q(inventory__lt=10))

    # ============================================
    # STEP 5: MULTIPLE OR CONDITIONS
    # ============================================
    # Get customers who are Gold OR Silver OR Bronze
    all_memberships = Customer.objects.filter(
        Q(membership='G') | Q(membership='S') | Q(membership='B')
    )

    # Get products in three price ranges
    specific_price_ranges = Product.objects.filter(
        Q(price__lte=30) |
        Q(price__range=(50, 70)) |
        Q(price__gte=120)
    )

    # ============================================
    # OUTPUT: Display results
    # ============================================
    return HttpResponse(f"""
        <h1>Django Q Objects - OR and AND Queries</h1>

        <h2>Step 1: OR Queries (|)</h2>
        <p>Products that are cheap OR expensive: {cheap_or_expensive.count()}</p>
        <p>Customers who are Gold OR Silver: {gold_or_silver.count()}</p>

        <h2>Step 2: AND Queries (&)</h2>
        <p>Products that are expensive AND low stock: {expensive_and_low_stock.count()}</p>

        <h2>Step 3: Combining OR and AND</h2>
        <p>Complex query results: {complex_query.count()}</p>

        <h2>Step 4: NOT Queries (~)</h2>
        <p>Products that are NOT cheap: {not_cheap.count()}</p>
        <p>Customers who are NOT Gold: {not_gold.count()}</p>

        <h2>Step 5: Multiple OR Conditions</h2>
        <p>All membership types: {all_memberships.count()}</p>
        <p>Products in specific price ranges: {specific_price_ranges.count()}</p>

        <hr>
        <h3>Quick Reference:</h3>
        <ul>
            <li>| = OR operator</li>
            <li>& = AND operator</li>
            <li>~ = NOT operator</li>
        </ul>
    """)


def f_objects_demo(request):
    """
    Demonstrates F objects for referencing field values in queries.
    F objects allow you to reference and compare database fields directly.
    """

    # ============================================
    # STEP 1: COMPARING FIELDS - Compare two fields in same model
    # ============================================
    # Get products where inventory is less than 10
    # (comparing a field value with a number)
    low_inventory = Product.objects.filter(inventory__lt=10)

    # Using F to reference field values
    # Get products where inventory equals price (field to field comparison)
    inventory_equals_price = Product.objects.filter(inventory=F('price'))

    # ============================================
    # STEP 2: FIELD ARITHMETIC - Do math with field values
    # ============================================
    # Get products where price is greater than inventory * 10
    price_gt_inventory_x10 = Product.objects.filter(
        price__gt=F('inventory') * 10)

    # Get products where price is less than inventory * 2
    price_lt_inventory_x2 = Product.objects.filter(
        price__lt=F('inventory') * 2)

    # Get products where inventory + 100 is greater than price
    inventory_plus_100 = Product.objects.filter(
        price__lt=F('inventory') + 100)

    # ============================================
    # STEP 3: COMBINING F and Q OBJECTS
    # ============================================
    # Get products where (price > 100 AND inventory < 20) OR (price < inventory * 5)
    complex_f_q = Product.objects.filter(
        Q(price__gt=100, inventory__lt=20) |
        Q(price__lt=F('inventory') * 5)
    )

    # Get products where price is between inventory and inventory * 10
    price_in_range = Product.objects.filter(
        price__gte=F('inventory'),
        price__lte=F('inventory') * 10
    )

    # ============================================
    # STEP 4: PRACTICAL EXAMPLES
    # ============================================
    # Get products that are "undervalued" (price less than half their inventory count)
    undervalued = Product.objects.filter(price__lt=F('inventory') / 2)

    # Get products that are "overpriced" (price more than 20 times inventory)
    overpriced = Product.objects.filter(price__gt=F('inventory') * 20)

    # Get products where we need to restock (inventory very low compared to typical price point)
    need_restock = Product.objects.filter(
        inventory__lt=10,
        price__gt=50  # High-value items with low stock
    )

    # ============================================
    # OUTPUT: Display results
    # ============================================
    return HttpResponse(f"""
        <h1>Django F Objects - Field References</h1>

        <h2>Step 1: Comparing Fields</h2>
        <p>Products with low inventory (&lt;10): {low_inventory.count()}</p>
        <p>Products where inventory = price: {inventory_equals_price.count()}</p>

        <h2>Step 2: Field Arithmetic</h2>
        <p>Products where price &gt; inventory × 10: {price_gt_inventory_x10.count()}</p>
        <p>Products where price &lt; inventory × 2: {price_lt_inventory_x2.count()}</p>

        <h2>Step 3: Combining F and Q Objects</h2>
        <p>Complex F+Q query results: {complex_f_q.count()}</p>
        <p>Price between inventory and inventory × 10: {price_in_range.count()}</p>

        <h2>Step 4: Practical Examples</h2>
        <p>Undervalued products (price &lt; inventory/2): {undervalued.count()}</p>
        <p>Overpriced products (price &gt; inventory × 20): {overpriced.count()}</p>
        <p>High-value items needing restock: {need_restock.count()}</p>

        <hr>
        <h3>Quick Reference:</h3>
        <ul>
            <li>F('field_name') - Reference a field value</li>
            <li>F('field') * 2 - Multiply field value</li>
            <li>F('field') + 10 - Add to field value</li>
            <li>F('field1') - F('field2') - Subtract fields</li>
        </ul>
    """)


def field_lookups_demo(request):
    """
    Demonstrates advanced field lookups and query methods.
    Shows contains, startswith, endswith, icontains, range, and more.
    """

    # ============================================
    # STEP 1: STRING LOOKUPS - Search text fields
    # ============================================
    # Get customers whose first name starts with 'J'
    starts_with_j = Customer.objects.filter(first_name__startswith='J')

    # Get customers whose first name ends with 'n'
    ends_with_n = Customer.objects.filter(first_name__endswith='n')

    # Get customers whose email contains 'gmail'
    gmail_users = Customer.objects.filter(email__contains='gmail')

    # Case-insensitive contains (icontains)
    gmail_users_ci = Customer.objects.filter(email__icontains='GMAIL')

    # ============================================
    # STEP 2: RANGE LOOKUPS - Find values in range
    # ============================================
    # Get products with price between 50 and 100
    mid_range_products = Product.objects.filter(price__range=(50, 100))

    # Get products with inventory between 10 and 50
    medium_stock = Product.objects.filter(inventory__range=(10, 50))

    # ============================================
    # STEP 3: NULL CHECKS - Find null/empty values
    # ============================================
    # Get customers with null email (if any)
    no_email = Customer.objects.filter(email__isnull=True)

    # Get customers with email (not null)
    has_email = Customer.objects.filter(email__isnull=False)

    # ============================================
    # STEP 4: IN LOOKUPS - Match against list of values
    # ============================================
    # Get customers with Gold or Silver membership
    premium_members = Customer.objects.filter(membership__in=['G', 'S'])

    # Get products with specific price points
    specific_prices = Product.objects.filter(price__in=[29.99, 49.99, 99.99])

    # ============================================
    # STEP 5: GREATER THAN / LESS THAN (with dates if you had them)
    # ============================================
    # Greater than or equal to
    expensive = Product.objects.filter(price__gte=100)

    # Less than or equal to
    affordable = Product.objects.filter(price__lte=50)

    # ============================================
    # STEP 6: COMBINING MULTIPLE LOOKUPS
    # ============================================
    # Get Gmail users with Gold membership
    gmail_gold = Customer.objects.filter(
        email__icontains='gmail',
        membership='G'
    )

    # Get mid-priced products with good stock
    good_inventory_mid_price = Product.objects.filter(
        price__range=(30, 80),
        inventory__gte=20
    )

    # ============================================
    # OUTPUT: Display results
    # ============================================
    return HttpResponse(f"""
        <h1>Django Field Lookups - Advanced Queries</h1>

        <h2>Step 1: String Lookups</h2>
        <p>Names starting with 'J': {starts_with_j.count()}</p>
        <p>Names ending with 'n': {ends_with_n.count()}</p>
        <p>Gmail users (case-sensitive): {gmail_users.count()}</p>
        <p>Gmail users (case-insensitive): {gmail_users_ci.count()}</p>

        <h2>Step 2: Range Lookups</h2>
        <p>Products priced $50-$100: {mid_range_products.count()}</p>
        <p>Products with 10-50 inventory: {medium_stock.count()}</p>

        <h2>Step 3: Null Checks</h2>
        <p>Customers without email: {no_email.count()}</p>
        <p>Customers with email: {has_email.count()}</p>

        <h2>Step 4: IN Lookups</h2>
        <p>Premium members (Gold/Silver): {premium_members.count()}</p>
        <p>Products at specific price points: {specific_prices.count()}</p>

        <h2>Step 6: Combined Lookups</h2>
        <p>Gmail users with Gold membership: {gmail_gold.count()}</p>
        <p>Mid-priced products with good stock: {good_inventory_mid_price.count()}</p>

        <hr>
        <h3>Common Field Lookups:</h3>
        <ul>
            <li>__exact - Exact match (default)</li>
            <li>__iexact - Case-insensitive exact match</li>
            <li>__contains - Contains substring</li>
            <li>__icontains - Case-insensitive contains</li>
            <li>__startswith - Starts with</li>
            <li>__endswith - Ends with</li>
            <li>__gt / __gte - Greater than / Greater or equal</li>
            <li>__lt / __lte - Less than / Less or equal</li>
            <li>__range - Between two values</li>
            <li>__in - In a list of values</li>
            <li>__isnull - Is null/not null</li>
        </ul>
    """)


def aggregation_methods_demo(request):
    """
    Demonstrates sorting, limiting, aggregation, and other advanced query methods.
    """

    # ============================================
    # SORTING & ORDERING
    # ============================================
    products_asc = Product.objects.order_by('price')
    products_desc = Product.objects.order_by('-price')
    multi_order = Product.objects.order_by('price', '-inventory')
    reversed_order = Product.objects.order_by('price').reverse()

    # ============================================
    # LIMITING & SLICING
    # ============================================
    first_5 = Product.objects.all()[:5]
    products_5_to_10 = Product.objects.all()[5:10]
    first_product = Product.objects.first()
    last_product = Product.objects.last()

    # ============================================
    # AGGREGATION - Calculate across all records
    # ============================================
    total_count = Product.objects.count()
    total_value = Product.objects.aggregate(total=Sum('price'))
    avg_price = Product.objects.aggregate(average=Avg('price'))
    price_range = Product.objects.aggregate(
        max_price=Max('price'), min_price=Min('price'))

    # ============================================
    # ANNOTATION - Add calculated fields
    # ============================================
    products_with_total = Product.objects.annotate(
        total_value=ExpressionWrapper(F('price') * F('inventory'), output_field=DecimalField()))

    # Using Concat() to combine text fields
    customers_with_fullname = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )

    # ============================================
    # VALUES & VALUES_LIST
    # ============================================
    product_dicts = Product.objects.values('title', 'price')[:3]
    product_tuples = Product.objects.values_list('title', 'price')[:3]
    all_prices = Product.objects.values_list('price', flat=True)

    # ============================================
    # DISTINCT - Remove duplicates
    # ============================================
    unique_prices = Product.objects.values_list('price', flat=True).distinct()

    # ============================================
    # EXISTS - Check existence
    # ============================================
    has_expensive = Product.objects.filter(price__gt=100).exists()

    # ============================================
    # ONLY & DEFER - Optimize queries
    # ============================================
    products_light = Product.objects.only('title', 'price')[:3]
    products_defer = Product.objects.defer('description')[:3]

    # ============================================
    # UNION - Combine querysets
    # ============================================
    expensive = Product.objects.filter(price__gt=100)
    low_stock = Product.objects.filter(inventory__lt=10)
    combined = expensive.union(low_stock)

    # ============================================
    # OUTPUT
    # ============================================
    return HttpResponse(f"""
        <h1>Aggregation & Advanced Query Methods</h1>

        <h2>Sorting & Ordering</h2>
        <p>Ascending: {products_asc.count()} | Multi-order: {multi_order.count()}</p>

        <h2>Limiting & Slicing</h2>
        <p>First 5: {len(first_5)} | First: {first_product.title if first_product else 'None'}</p>

        <h2>Aggregation</h2>
        <p>Count: {total_count} | Avg: ${avg_price.get('average', 0):.2f}</p>
        <p>Range: ${price_range.get('min_price', 0)} - ${price_range.get('max_price', 0)}</p>

        <h2>Annotation</h2>
        <p>Annotated products: {products_with_total.count()}</p>
        <p>Concat example: {list(customers_with_fullname.values('full_name')[:3])}</p>

        <h2>Values & Distinct</h2>
        <p>Unique prices: {unique_prices.count()}</p>

        <h2>Exists & Union</h2>
        <p>Has expensive: {has_expensive} | Combined: {combined.count()}</p>

        <hr>
        <h3>Methods Reference:</h3>
        <ul>
            <li><b>order_by()</b> - Sort | <b>reverse()</b> - Reverse</li>
            <li><b>first() / last()</b> - Get first/last</li>
            <li><b>[start:end]</b> - Slice results</li>
            <li><b>aggregate(Sum, Avg, Max, Min, Count)</b> - Calculate</li>
            <li><b>annotate()</b> - Add calculated fields</li>
            <li><b>Concat()</b> - Combine text fields</li>
            <li><b>values() / values_list()</b> - Dicts/tuples</li>
            <li><b>distinct()</b> - Remove duplicates</li>
            <li><b>exists()</b> - Check existence</li>
            <li><b>only() / defer()</b> - Optimize loading</li>
            <li><b>union()</b> - Combine querysets</li>
        </ul>
    """)


def annotate_values_demo(request):
    """
    How annotate() and values() work
    ======================================


    annotate() adds a new computed field to each object in your queryset. It doesn't change
    the database, just adds the field temporarily to each result.




    values() returns dictionaries instead of model instances. Great for when you only need
    specific fields, not the full object.
    """

    # ============================================
    # ANNOTATE - Add calculated fields to each object
    # ============================================
    # Without annotate - manual calculation
    products = Product.objects.all()
    # for product in products:
    #     total_value = product.price * product.inventory  # Manual

    # With annotate - Django calculates it for you
    products_with_value = Product.objects.annotate(
        inventory_value=ExpressionWrapper(
            F('price') * F('inventory'), output_field=DecimalField())
    )
    # Now each product has .inventory_value attribute

    # Annotate with multiple calculations
    products_multi = Product.objects.annotate(
        inventory_value=ExpressionWrapper(
            F('price') * F('inventory'), output_field=DecimalField()),
        double_price=ExpressionWrapper(
            F('price') * 2, output_field=DecimalField()),
        half_inventory=ExpressionWrapper(
            F('inventory') / 2, output_field=DecimalField())
    )

    # Using Value() to add static values
    products_with_static = Product.objects.annotate(
        discount_percent=Value(10),  # Add static value
        currency=Value('USD'),  # Add static string
        discounted_price=ExpressionWrapper(
            F('price') * Value(0.9), output_field=DecimalField())
    )

    # ============================================
    # VALUES - Get dictionaries instead of objects
    # ============================================
    # Without values - returns Product objects
    products_objects = Product.objects.all()[:3]
    # for product in products_objects:
    #     print(product.title, product.price)  # Access via attributes

    # With values - returns dictionaries
    products_dicts = Product.objects.values('title', 'price')[:3]
    # for product in products_dicts:
    #     print(product['title'], product['price'])  # Access like dict
    # Returns: [{'title': 'Laptop', 'price': 999.99}, ...]

    # ============================================
    # VALUES_LIST - Returns tuples instead of dicts
    # ============================================
    # Returns tuples
    products_tuples = Product.objects.values_list('title', 'price')[:3]
    # Returns: [('Laptop', 999.99), ('Mouse', 29.99)]

    # With flat=True - only works with single field
    all_prices = Product.objects.values_list('price', flat=True)[:5]
    # Returns: [999.99, 29.99, 49.99, ...]

    # ============================================
    # COMBINING annotate() + values()
    # ============================================
    # Get only title and calculated inventory value as dictionaries
    calculated_dicts = Product.objects.annotate(
        inventory_value=ExpressionWrapper(
            F('price') * F('inventory'), output_field=DecimalField())
    ).values('title', 'inventory_value')[:3]
    # Returns: [{'title': 'Laptop', 'inventory_value': 49999.50}, ...]

    # Combine with values_list for tuples
    calculated_tuples = Product.objects.annotate(
        inventory_value=ExpressionWrapper(
            F('price') * F('inventory'), output_field=DecimalField())
    ).values_list('title', 'inventory_value')[:3]

    # ============================================
    # OUTPUT
    # ============================================
    return HttpResponse(f"""
annotate() - Add Calculated Fields:
{list(products_with_value.values('title', 'inventory_value')[:3])}

annotate() with Value() - Add Static Values:
{list(products_with_static.values('title', 'price', 'discount_percent', 'currency', 'discounted_price')[:3])}

values() - Get Dictionaries:
{list(products_dicts)}

values_list() - Get Tuples:
{list(products_tuples)}

values_list(flat=True) - Flat List:
{list(all_prices)}

Combining annotate() + values():
{list(calculated_dicts)}

Combining annotate() + values_list():
{list(calculated_tuples)}
    """)


def select_prefetch_demo(request):
    """
    How select_related and prefetch_related work
    """

    # ============================================
    # THE N+1 QUERY PROBLEM (INEFFICIENT)
    # ============================================
    # Without select_related - INEFFICIENT
    products_bad = Product.objects.all()[:5]  # 1 query to get products

    # for product in products_bad:
    #     print(product.collection.title)  # 1 query PER product!
    #     # If you have 100 products = 1 + 100 = 101 queries! 😱

    # ============================================
    # SELECT_RELATED - For ForeignKey and OneToOne
    # ============================================
    # With select_related - EFFICIENT
    # Use for FORWARD ForeignKey relationships
    # Performs SQL JOIN - fetches related data in SINGLE query

    products_with_collection = Product.objects.select_related('collection')[:5]
    # 1 query with JOIN to get products AND collections together

    # for product in products_with_collection:
    #     print(product.collection.title)  # NO extra queries!
    # Total: Just 1 query! 🎉

    # Multiple levels deep
    # products_deep = Product.objects.select_related('collection__parent')
    # Joins through multiple tables: products -> collections -> parent_category

    # Multiple relations at once
    # products_multi = Product.objects.select_related('collection', 'supplier')
    # Joins products with BOTH collection AND supplier in 1 query

    # ============================================
    # PREFETCH_RELATED - For ManyToMany and Reverse ForeignKey
    # ============================================
    # Without prefetch_related - INEFFICIENT
    # customers = Customer.objects.all()[:3]  # 1 query
    # for customer in customers:
    #     for order in customer.orders.all():  # 1 query PER customer!
    #         print(order.placed_at)
    # If 3 customers = 1 + 3 = 4 queries! 😱

    # With prefetch_related - EFFICIENT
    # Use for REVERSE ForeignKey and ManyToMany relationships
    # Uses separate queries but with optimized IN clause

    customers_with_orders = Customer.objects.prefetch_related('orders')[:3]
    # Query 1: Get all customers
    # Query 2: Get all orders WHERE customer_id IN (1, 2, 3)
    # Total: 2 queries (not N+1) 🎉

    # for customer in customers_with_orders:
    #     for order in customer.orders.all():  # NO extra queries!
    #         print(order.placed_at)

    # Get collections with their products (reverse ForeignKey)
    collections_with_products = Collection.objects.prefetch_related('products')[
        :3]
    # Query 1: Get collections
    # Query 2: Get all products WHERE collection_id IN (1, 2, 3)

    # for collection in collections_with_products:
    #     for product in collection.products.all():  # NO extra queries!
    #         print(product.title)

    # ============================================
    # COMBINING BOTH
    # ============================================
    # You can use BOTH together when needed
    orders_optimized = Order.objects.select_related('customer').all()[:5]
    # select_related for customer (ForeignKey forward)
    # Gets orders AND their customers in 1 query with JOIN

    # Complex example (if you had more relations):
    # orders_complex = Order.objects.select_related('customer').prefetch_related('items')
    # Query 1: Orders + Customer (JOIN)
    # Query 2: All order items WHERE order_id IN (...)

    # ============================================
    # COMPARISON SUMMARY
    # ============================================

    # BAD: N+1 queries (without optimization)
    bad_products = Product.objects.all()[:5]  # 1 query
    # Accessing product.collection causes 1 query PER product = 6 queries total! 😱

    # GOOD: 1 query with JOIN (select_related)
    good_products = Product.objects.select_related('collection')[:5]  # 1 query
    # Accessing product.collection = 0 extra queries! ✅

    # GOOD: 2 queries (prefetch_related)
    good_customers = Customer.objects.prefetch_related('orders')[
        :3]  # 2 queries
    # Accessing customer.orders.all() = 0 extra queries! ✅

    # ============================================
    # OUTPUT
    # ============================================
    return HttpResponse(f"""
select_related (ForeignKey - Forward relation):
Products with collection: {good_products.count()}
SQL: Single query with JOIN

prefetch_related (Reverse ForeignKey):
Customers with orders: {good_customers.count()}
SQL: Separate queries with IN clause

Combining both:
Orders with customer: {orders_optimized.count()}

Key Differences:
- select_related: ForeignKey, OneToOne (SQL JOIN, 1 query)
- prefetch_related: ManyToMany, Reverse FK (Separate queries, Python join)

When to use:
- product.collection → select_related('collection')
- customer.orders.all() → prefetch_related('orders')
- collection.products.all() → prefetch_related('products')
    """)


def crud_operations_demo(request):
    """
    CRUD: Create, Read, Update, Delete operations
    """

    # ============================================
    # CREATE - Adding new objects to database
    # ============================================

    # Method 1: Create and save in one step
    collection = Collection.objects.create(
        title='Electronics'
    )
    # Automatically saves to database

    # Method 2: Create object, then save manually
    collection2 = Collection(title='Books')
    collection2.save()  # Save to database

    # Method 3: Bulk create (multiple objects at once - more efficient)
    Collection.objects.bulk_create([
        Collection(title='Clothing'),
        Collection(title='Food'),
        Collection(title='Toys'),
    ])
    # Inserts all in single query - very fast!

    # Create related objects
    product = Product.objects.create(
        title='Laptop',
        description='Gaming laptop',
        price=Decimal('999.99'),
        inventory=50,
        collection=collection  # Link to collection
    )


    # ============================================
    # READ - Getting objects from database
    # ============================================

    # Get single object by ID
    try:
        product_1 = Product.objects.get(id=1)
    except Product.DoesNotExist:
        product_1 = None

    # Get single object by field
    try:
        electronics = Collection.objects.get(title='Electronics')
    except Collection.DoesNotExist:
        electronics = None

    # Get all objects
    all_products = Product.objects.all()

    # Filter objects (returns QuerySet)
    expensive_products = Product.objects.filter(price__gt=100)

    # Get first/last
    first_product = Product.objects.first()
    last_product = Product.objects.last()

    # Check if exists
    has_products = Product.objects.filter(price__gt=1000).exists()


    # ============================================
    # UPDATE - Modifying existing objects
    # ============================================

    # Method 1: Get object, modify, save
    if product_1:
        product_1.price = Decimal('899.99')
        product_1.inventory = 45
        product_1.save()  # Updates database

    # Method 2: Update multiple objects at once (more efficient)
    # Increase price of all electronics by 10%
    Product.objects.filter(collection__title='Electronics').update(
        price=F('price') * 1.1
    )
    # Updates all matching records in single query

    # Update all products in collection
    Product.objects.filter(collection=collection).update(
        inventory=F('inventory') + 10
    )

    # Update single field for all
    Product.objects.all().update(last_update=models.functions.Now())


    # ============================================
    # DELETE - Removing objects from database
    # ============================================

    # Method 1: Get object, then delete
    try:
        old_product = Product.objects.get(title='Old Product')
        old_product.delete()
    except Product.DoesNotExist:
        pass

    # Method 2: Delete multiple objects at once
    # Delete all products with zero inventory
    deleted_count = Product.objects.filter(inventory=0).delete()
    # Returns (count, {model: count})

    # Delete all products in a collection
    # Product.objects.filter(collection__title='Discontinued').delete()

    # Delete single collection (if no PROTECT constraint)
    # Collection.objects.filter(title='Temp').delete()


    # ============================================
    # GET_OR_CREATE - Get existing or create new
    # ============================================

    # Get existing or create if doesn't exist
    gaming_collection, created = Collection.objects.get_or_create(
        title='Gaming',
        defaults={'featured_product': None}  # Only used if creating
    )
    # created = True if new, False if existing


    # ============================================
    # UPDATE_OR_CREATE - Update existing or create new
    # ============================================

    # Update if exists, create if doesn't
    product_obj, created = Product.objects.update_or_create(
        title='Gaming Mouse',  # Lookup field
        defaults={
            'price': Decimal('49.99'),
            'inventory': 100,
            'description': 'RGB Gaming Mouse',
            'collection': gaming_collection
        }
    )
    # Updates if found, creates if not found


    # ============================================
    # OUTPUT
    # ============================================
    return HttpResponse(f"""
CRUD Operations Demo

CREATE:
- Created collections: {Collection.objects.count()}
- Created products: {Product.objects.count()}
- Methods: create(), save(), bulk_create()

READ:
- All products: {all_products.count()}
- Expensive products (>100): {expensive_products.count()}
- First product: {first_product.title if first_product else 'None'}
- Has expensive items: {has_products}

UPDATE:
- Updated product price: {product_1.price if product_1 else 'N/A'}
- Methods: save(), update(), F() expressions

DELETE:
- Deleted items: {deleted_count}
- Methods: delete(), filter().delete()

GET_OR_CREATE:
- Gaming collection created: {created}

UPDATE_OR_CREATE:
- Gaming Mouse updated/created: {created}

Key Methods:
- CREATE: .create(), .save(), .bulk_create()
- READ: .get(), .filter(), .all(), .first(), .last(), .exists()
- UPDATE: .save(), .update(), .update_or_create()
- DELETE: .delete()
- UTILITY: .get_or_create(), .update_or_create()
    """)


def transactions_demo(request):
    """
    Database Transactions - Ensure all-or-nothing operations
    """

    # ============================================
    # WHY TRANSACTIONS?
    # ============================================
    # Transactions ensure multiple database operations either:
    # - ALL succeed (commit)
    # - ALL fail and rollback (undo everything)
    # This prevents partial updates that leave data inconsistent


    # ============================================
    # METHOD 1: transaction.atomic() - Decorator
    # ============================================
    # Use @transaction.atomic decorator for entire function
    # If ANY error occurs, ALL changes are rolled back

    @transaction.atomic
    def create_order_atomic():
        # Create order
        customer = Customer.objects.first()
        if customer:
            order = Order.objects.create(customer=customer)

            # Deduct inventory for products
            product = Product.objects.first()
            if product:
                product.inventory -= 1
                product.save()

            # If error occurs here, BOTH order and inventory changes are rolled back
            # raise Exception("Something went wrong!")  # Uncomment to test rollback

            return order
        return None


    # ============================================
    # METHOD 2: transaction.atomic() - Context Manager
    # ============================================
    # Use 'with' statement for specific code blocks

    try:
        with transaction.atomic():
            # Everything inside this block is atomic

            # Create a collection
            collection = Collection.objects.create(title='Transaction Test Collection')

            # Create products in that collection
            Product.objects.create(
                title='Transaction Test Product 1',
                price=Decimal('100.00'),
                inventory=10,
                description='Test',
                collection=collection
            )

            Product.objects.create(
                title='Transaction Test Product 2',
                price=Decimal('200.00'),
                inventory=20,
                description='Test',
                collection=collection
            )

            # If error occurs here, collection and BOTH products are NOT saved
            # raise ValueError("Test error")  # Uncomment to test rollback

    except Exception as e:
        # Transaction was rolled back
        error_msg = f"Transaction failed: {e}"
    else:
        error_msg = "Transaction succeeded"


    # ============================================
    # METHOD 3: SAVEPOINTS - Partial Rollback
    # ============================================
    # Savepoints allow you to rollback to a specific point, not everything

    try:
        with transaction.atomic():
            # Create customer (this will be saved)
            customer = Customer.objects.create(
                first_name='John',
                last_name='Doe',
                email='john.transaction@test.com',
                phone='1234567890'
            )

            # Create a savepoint
            sid = transaction.savepoint()

            try:
                # Try to create order (might fail)
                order = Order.objects.create(customer=customer)

                # Simulate error
                # raise Exception("Order creation failed")

                # If successful, commit the savepoint
                transaction.savepoint_commit(sid)

            except Exception as e:
                # Rollback ONLY to savepoint (customer is still saved)
                transaction.savepoint_rollback(sid)

    except Exception as e:
        pass


    # ============================================
    # PRACTICAL EXAMPLE: Transfer Money
    # ============================================
    # Transfer inventory between two products (must be atomic)

    def transfer_inventory(from_product_id, to_product_id, amount):
        with transaction.atomic():
            # Lock rows to prevent race conditions
            from_product = Product.objects.select_for_update().get(id=from_product_id)
            to_product = Product.objects.select_for_update().get(id=to_product_id)

            # Check sufficient inventory
            if from_product.inventory < amount:
                raise ValueError("Insufficient inventory")

            # Transfer
            from_product.inventory -= amount
            to_product.inventory += amount

            from_product.save()
            to_product.save()

            # Both succeed or both fail - no partial transfer!


    # ============================================
    # WHEN TO USE TRANSACTIONS
    # ============================================
    # 1. Creating related objects (Order + OrderItems)
    # 2. Transferring resources (money, inventory)
    # 3. Updates that depend on each other
    # 4. Any operation where partial completion would be bad


    # ============================================
    # TRANSACTION ISOLATION
    # ============================================
    # select_for_update() locks rows during transaction
    # Prevents other transactions from modifying same data

    try:
        with transaction.atomic():
            # Lock product row until transaction completes
            product = Product.objects.select_for_update().get(id=1)
            product.inventory += 10
            product.save()
            # Other transactions must wait until this commits
    except Product.DoesNotExist:
        pass


    # ============================================
    # OUTPUT
    # ============================================
    return HttpResponse(f"""
Database Transactions Demo

WHAT ARE TRANSACTIONS?
- Ensure all-or-nothing operations
- Either ALL changes succeed OR ALL are rolled back
- Prevents partial/inconsistent data updates

METHOD 1: @transaction.atomic decorator
- Wrap entire function in transaction
- Automatic rollback on any exception

METHOD 2: with transaction.atomic() context manager
- Wrap specific code blocks
- More control over transaction scope
- Result: {error_msg}

METHOD 3: Savepoints
- Partial rollback within transaction
- Rollback to specific point, not everything
- Useful for complex multi-step operations

PRACTICAL USE CASES:
1. Creating order with items (all or nothing)
2. Transferring inventory/money between accounts
3. Updating multiple related records
4. Any operation requiring consistency

ROW LOCKING:
- select_for_update() locks rows during transaction
- Prevents race conditions
- Other transactions wait until lock released

KEY POINTS:
- Use transactions for critical operations
- Smaller transactions = better performance
- Locks can cause deadlocks if not careful
- Always handle exceptions properly

Example: Transfer Inventory
with transaction.atomic():
    product1 = Product.objects.select_for_update().get(id=1)
    product2 = Product.objects.select_for_update().get(id=2)
    product1.inventory -= 10
    product2.inventory += 10
    product1.save()
    product2.save()
    # Both updates succeed or both fail!
    """)
