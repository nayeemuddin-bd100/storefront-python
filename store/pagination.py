from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    page_size = 3  # Default number of items per page
