from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class DistributionsLimitOffsetPaginator(LimitOffsetPagination):
    default_limit = 50

class DistributionsPageNumberPaginator(PageNumberPagination):
    page_size = 50
