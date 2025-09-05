"""
自定义分页器
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from datetime import datetime
from django.core.paginator import Paginator


class CustomPageNumberPagination(PageNumberPagination):
    """自定义分页器"""
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """返回自定义分页响应格式"""
        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'results': data,
                'pagination': {
                    'page': self.page.number,
                    'page_size': self.page.paginator.per_page,
                    'total': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages,
                    'has_next': self.page.has_next(),
                    'has_previous': self.page.has_previous(),
                    'next_page': self.page.next_page_number() if self.page.has_next() else None,
                    'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,
                }
            },
            'timestamp': datetime.now().isoformat()
        })
    
    def get_paginated_response_schema(self, schema):
        """返回分页响应的schema"""
        return {
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'integer',
                    'example': 200,
                },
                'message': {
                    'type': 'string',
                    'example': 'success',
                },
                'data': {
                    'type': 'object',
                    'properties': {
                        'results': schema,
                        'pagination': {
                            'type': 'object',
                            'properties': {
                                'page': {
                                    'type': 'integer',
                                    'example': 1,
                                },
                                'page_size': {
                                    'type': 'integer',
                                    'example': 20,
                                },
                                'total': {
                                    'type': 'integer',
                                    'example': 100,
                                },
                                'total_pages': {
                                    'type': 'integer',
                                    'example': 5,
                                },
                                'has_next': {
                                    'type': 'boolean',
                                    'example': True,
                                },
                                'has_previous': {
                                    'type': 'boolean',
                                    'example': False,
                                },
                                'next_page': {
                                    'type': 'integer',
                                    'example': 2,
                                },
                                'previous_page': {
                                    'type': 'integer',
                                    'example': None,
                                },
                            }
                        }
                    }
                },
                'timestamp': {
                    'type': 'string',
                    'format': 'date-time',
                },
            }
        }


def paginate_queryset(queryset, request, page_size=20):
    """
    简单的分页函数

    Args:
        queryset: Django QuerySet对象
        request: HTTP请求对象
        page_size: 每页数量，默认20

    Returns:
        dict: 包含分页结果的字典
    """
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', page_size))

    # 限制最大页面大小
    if page_size > 100:
        page_size = 100

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    return {
        'results': page_obj.object_list,
        'total': paginator.count,
        'page': page,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
    }
