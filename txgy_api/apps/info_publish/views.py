"""
信息发布视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from utils.response import success_response, error_response

# TODO: 添加信息发布相关视图

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supply_list(request):
    """供应信息列表"""
    return success_response([], message='供应信息列表')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def supply_create(request):
    """创建供应信息"""
    return success_response({}, message='供应信息创建成功')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def demand_list(request):
    """采购需求列表"""
    return success_response([], message='采购需求列表')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def demand_create(request):
    """创建采购需求"""
    return success_response({}, message='采购需求创建成功')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recruitment_list(request):
    """招聘信息列表"""
    return success_response([], message='招聘信息列表')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recruitment_create(request):
    """创建招聘信息"""
    return success_response({}, message='招聘信息创建成功')
