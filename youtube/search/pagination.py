from rest_framework.pagination import PageNumberPagination

# creating a pagination class
class VideoPagination(PageNumberPagination):
    page_size = 10