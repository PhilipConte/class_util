from rest_framework.pagination import LimitOffsetPagination

class DistributionsLimitOffsetPaginator(LimitOffsetPagination):
    default_limit = 25
    max_limit = 50
