"""
统一响应格式工具
"""
from rest_framework.response import Response
from datetime import datetime
import uuid


def success_response(data=None, message="success", code=200):
    """
    成功响应格式
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 状态码
    
    Returns:
        Response: DRF响应对象
    """
    return Response({
        "code": code,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat(),
        "request_id": str(uuid.uuid4())
    }, status=code)


def error_response(message, code=400, errors=None):
    """
    错误响应格式
    
    Args:
        message: 错误消息
        code: 错误码
        errors: 详细错误信息
    
    Returns:
        Response: DRF响应对象
    """
    response_data = {
        "code": code,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "request_id": str(uuid.uuid4())
    }
    
    if errors:
        response_data["errors"] = errors
    
    return Response(response_data, status=code)


def paginated_response(data, pagination_info, message="success"):
    """
    分页响应格式
    
    Args:
        data: 分页数据
        pagination_info: 分页信息
        message: 响应消息
    
    Returns:
        Response: DRF响应对象
    """
    return Response({
        "code": 200,
        "message": message,
        "data": {
            "results": data,
            "pagination": pagination_info
        },
        "timestamp": datetime.now().isoformat(),
        "request_id": str(uuid.uuid4())
    }, status=200)
