"""
公共模块视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.response import success_response, error_response

@api_view(['GET'])
@permission_classes([AllowAny])
def region_list(request):
    """地区列表"""
    return success_response([], message='地区列表')

@api_view(['GET'])
@permission_classes([AllowAny])
def region_children(request, parent_code):
    """获取子地区"""
    return success_response([], message='子地区列表')

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """分类列表"""
    return success_response([], message='分类列表')

@api_view(['GET'])
@permission_classes([AllowAny])
def category_by_type(request, category_type):
    """按类型获取分类"""
    return success_response([], message='分类列表')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def file_upload(request):
    """文件上传"""
    return success_response({}, message='文件上传成功')

@api_view(['GET'])
@permission_classes([AllowAny])
def system_configs(request):
    """系统配置"""
    return success_response({}, message='系统配置')
