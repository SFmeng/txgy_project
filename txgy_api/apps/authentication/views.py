"""
用户认证视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
import random
import logging

from .models import User, Enterprise
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    PasswordChangeSerializer, PasswordResetSerializer, SmsCodeSerializer,
    UserManagementSerializer
)
from utils.response import success_response, error_response

logger = logging.getLogger('apps')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # 清除验证码缓存（如果有的话）
            phone = serializer.validated_data.get('phone')
            if phone:
                cache.delete(f'sms_code_{phone}')
            
            logger.info(f"用户注册成功: {user.username}")
            
            return success_response({
                'user_id': user.user_id,
                'username': user.username,
                'user_type': user.user_type,
                'status': user.status
            }, message='注册成功')
            
        except Exception as e:
            logger.error(f"用户注册失败: {str(e)}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return error_response(f'注册失败: {str(e)}', code=500)
    
    return error_response('注册失败', errors=serializer.errors, code=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        try:
            # 生成JWT Token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # 更新登录信息
            user.last_login = timezone.now()
            user.last_login_ip = get_client_ip(request)
            user.save(update_fields=['last_login', 'last_login_ip'])
            
            # 获取用户权限
            permissions = get_user_permissions(user)
            
            # 构建用户信息
            user_info = {
                'user_id': user.user_id,
                'username': user.username,
                'user_type': user.user_type,
                'real_name': user.real_name,
                'avatar': user.avatar.url if user.avatar else None,
                'permissions': permissions
            }
            
            # 如果是企业用户，添加企业信息
            if user.user_type == 'enterprise' and hasattr(user, 'enterprise'):
                user_info['enterprise_info'] = {
                    'company_name': user.enterprise.company_name,
                    'company_type': user.enterprise.company_type,
                    'enterprise_id': user.enterprise.enterprise_id,
                    'certification_status': user.enterprise.certification_status
                }
            
            logger.info(f"用户登录成功: {user.username}")
            
            return success_response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'expires_in': 86400,  # 24小时
                'user_info': user_info
            }, message='登录成功')
            
        except Exception as e:
            logger.error(f"用户登录失败: {str(e)}")
            return error_response('登录失败，请稍后重试', code=500)
    
    return error_response('登录失败', errors=serializer.errors, code=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """用户登出"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        logger.info(f"用户登出: {request.user.username}")
        return success_response(message='登出成功')
    except Exception as e:
        logger.error(f"用户登出失败: {str(e)}")
        return success_response(message='登出成功')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """获取用户信息"""
    serializer = UserProfileSerializer(request.user)
    return success_response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """更新用户信息"""
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"用户信息更新: {request.user.username}")
        return success_response(serializer.data, message='信息更新成功')
    
    return error_response('更新失败', errors=serializer.errors, code=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        
        logger.info(f"用户修改密码: {user.username}")
        return success_response(message='密码修改成功')
    
    return error_response('密码修改失败', errors=serializer.errors, code=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """重置密码"""
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']
        phone = serializer.validated_data['phone']
        
        user.set_password(new_password)
        user.save()
        
        # 清除验证码缓存
        cache.delete(f'sms_code_{phone}')
        
        logger.info(f"用户重置密码: {user.username}")
        return success_response(message='密码重置成功')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enterprise_verify(request):
    """企业认证审核"""
    from .models import Enterprise

    user_id = request.data.get('user_id')
    action = request.data.get('action')  # 'approve' 或 'reject'
    remark = request.data.get('remark', '')

    if not user_id or not action:
        return error_response('参数不完整')

    if action not in ['approve', 'reject']:
        return error_response('无效的操作类型')

    try:
        user = User.objects.get(user_id=user_id, user_type='enterprise')

        # 获取或创建企业信息
        enterprise, created = Enterprise.objects.get_or_create(
            user=user,
            defaults={
                'company_name': user.real_name or user.username,
                'company_type': 'manufacturer',
                'certification_status': 'pending'
            }
        )

        # 更新认证状态
        if action == 'approve':
            enterprise.certification_status = 'verified'
            message = '企业认证通过'
        else:
            enterprise.certification_status = 'rejected'
            message = '企业认证拒绝'
        enterprise.save()

        return success_response(message=message)

    except User.DoesNotExist:
        return error_response('用户不存在或不是企业用户')
    except Exception as e:
        return error_response(f'操作失败: {str(e)}')
    
    return error_response('密码重置失败', errors=serializer.errors, code=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_sms_code(request):
    """发送短信验证码"""
    serializer = SmsCodeSerializer(data=request.data)
    if serializer.is_valid():
        phone = serializer.validated_data['phone']
        sms_type = serializer.validated_data['type']
        
        # 检查发送频率限制
        cache_key = f'sms_limit_{phone}'
        if cache.get(cache_key):
            return error_response('发送过于频繁，请稍后再试', code=429)
        
        # 生成验证码
        code = str(random.randint(100000, 999999))
        
        # 存储验证码到缓存（5分钟有效）
        cache.set(f'sms_code_{phone}', code, 300)
        
        # 设置发送频率限制（60秒）
        cache.set(cache_key, True, 60)
        
        # TODO: 调用短信服务发送验证码
        # send_sms(phone, code, sms_type)
        
        logger.info(f"发送短信验证码: {phone}, 类型: {sms_type}")
        
        # 开发环境返回验证码（生产环境删除）
        response_data = {'message': '验证码发送成功'}
        if request.META.get('HTTP_HOST', '').startswith('localhost'):
            response_data['code'] = code  # 仅开发环境
        
        return success_response(response_data)
    
    return error_response('发送失败', errors=serializer.errors, code=400)


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_permissions(user):
    """获取用户权限列表"""
    from apps.organization.models import UserRole, RolePermission, RoleMenu

    try:
        # 获取用户角色
        user_roles = UserRole.objects.filter(user=user).select_related('role')

        if not user_roles.exists():
            # 如果用户没有角色，返回基础权限
            return {
                'permissions': ['basic_access'],
                'menus': []
            }

        # 获取所有角色的权限
        permissions = set()
        menus = []
        menu_ids = set()  # 用于去重

        for user_role in user_roles:
            role = user_role.role

            # 获取角色权限
            role_permissions = RolePermission.objects.filter(role=role).select_related('permission')
            for rp in role_permissions:
                permissions.add(rp.permission.perm_code)

            # 获取角色菜单
            role_menus = RoleMenu.objects.filter(role=role).select_related('menu')
            for rm in role_menus:
                menu = rm.menu
                if str(menu.menu_id) not in menu_ids:
                    menu_data = {
                        'menu_id': str(menu.menu_id),
                        'menu_name': menu.menu_name,
                        'path': menu.path,
                        'icon': menu.icon,
                        'sort': menu.sort,
                        'parent_id': str(menu.parent_id) if menu.parent_id else None,
                        'terminal': menu.terminal
                    }
                    menus.append(menu_data)
                    menu_ids.add(str(menu.menu_id))

        # 按排序号排序
        menu_list = sorted(menus, key=lambda x: x['sort'])

        return {
            'permissions': list(permissions),
            'menus': menu_list
        }

    except Exception as e:
        logger.error(f"获取用户权限失败: {str(e)}")
        return {
            'permissions': ['basic_access'],
            'menus': []
        }


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_management(request):
    """用户管理 - 列表和创建"""
    if request.method == 'GET':
        # 获取用户列表
        from utils.pagination import paginate_queryset
        from django.db.models import Q

        queryset = User.objects.select_related('enterprise').prefetch_related('userrole_set__role').all().order_by('-date_joined')

        # 搜索过滤
        username = request.GET.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)

        user_type = request.GET.get('user_type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)

        status = request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # 分页
        page_data = paginate_queryset(queryset, request)
        serializer = UserManagementSerializer(page_data['results'], many=True)

        return success_response({
            'results': serializer.data,
            'total': page_data['total'],
            'page': page_data['page'],
            'page_size': page_data['page_size']
        })

    elif request.method == 'POST':
        # 创建用户
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return success_response(
                    UserManagementSerializer(user).data,
                    message='用户创建成功'
                )
            except Exception as e:
                return error_response(f'创建失败: {str(e)}')
        return error_response('创建失败', errors=serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    """用户详情、更新和删除"""
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return error_response('用户不存在', code=404)

    if request.method == 'GET':
        serializer = UserManagementSerializer(user)
        return success_response(serializer.data)

    elif request.method == 'PUT':
        # 更新用户 - 只更新基本字段
        allowed_fields = ['real_name', 'email', 'phone', 'status', 'user_type']
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}

        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            user.save()
            serializer = UserManagementSerializer(user)
            return success_response(serializer.data, message='用户更新成功')
        except Exception as e:
            return error_response(f'更新失败: {str(e)}')

    elif request.method == 'DELETE':
        # 删除用户
        if user.username == 'admin':
            return error_response('不能删除管理员用户')

        user.delete()
        return success_response(message='用户删除成功')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Dashboard统计数据"""
    from django.db.models import Count, Q
    from datetime import datetime, timedelta

    try:
        # 获取今日日期
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # 用户统计
        total_users = User.objects.count()
        enterprise_users = User.objects.filter(user_type='enterprise').count()
        individual_users = User.objects.filter(user_type='individual').count()
        active_users = User.objects.filter(is_active=True).count()

        # 今日新增用户
        today_users = User.objects.filter(date_joined__date=today).count()

        # 企业认证统计
        verified_enterprises = Enterprise.objects.filter(certification_status='verified').count()
        pending_enterprises = Enterprise.objects.filter(certification_status='pending').count()

        # 模拟其他统计数据（后续可以根据实际业务模块补充）
        total_orders = 0  # 订单模块待实现
        total_revenue = 0  # 收入模块待实现
        total_messages = 0  # 消息模块待实现

        # 今日访问量（模拟数据，可以后续集成访问日志）
        today_visits = 1234

        stats_data = {
            'today_stats': {
                'visits': today_visits,
                'users': today_users,
                'orders': 0  # 待实现
            },
            'overview_stats': [
                {
                    'key': 'users',
                    'title': '用户总数',
                    'value': str(total_users),
                    'trend': 12.5,  # 可以后续计算真实增长率
                    'color': '#409EFF',
                    'icon': 'User'
                },
                {
                    'key': 'enterprises',
                    'title': '企业用户',
                    'value': str(enterprise_users),
                    'trend': 8.2,
                    'color': '#67C23A',
                    'icon': 'Shop'
                },
                {
                    'key': 'verified',
                    'title': '认证企业',
                    'value': str(verified_enterprises),
                    'trend': -2.1,
                    'color': '#E6A23C',
                    'icon': 'DataBoard'
                },
                {
                    'key': 'active',
                    'title': '活跃用户',
                    'value': str(active_users),
                    'trend': 15.3,
                    'color': '#F56C6C',
                    'icon': 'ChatDotRound'
                }
            ],
            'user_stats': {
                'total_users': total_users,
                'enterprise_users': enterprise_users,
                'individual_users': individual_users,
                'verified_enterprises': verified_enterprises,
                'pending_enterprises': pending_enterprises
            }
        }

        return success_response(stats_data, message='统计数据获取成功')

    except Exception as e:
        logger.error(f"获取统计数据失败: {str(e)}")
        return error_response(f'获取统计数据失败: {str(e)}', code=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """获取用户权限和菜单"""
    try:
        user_data = get_user_permissions(request.user)

        # 构建树形菜单结构
        menus = user_data['menus']
        menu_tree = []
        menu_map = {}

        # 先创建所有菜单项的映射
        for menu in menus:
            menu_item = {
                'menu_id': menu['menu_id'],
                'menu_name': menu['menu_name'],
                'path': menu['path'],
                'icon': menu['icon'],
                'sort': menu['sort'],
                'parent_id': menu['parent_id'],
                'terminal': menu['terminal'],
                'children': []
            }
            menu_map[menu['menu_id']] = menu_item

        # 构建树形结构
        for menu in menus:
            menu_item = menu_map[menu['menu_id']]
            if menu['parent_id'] and menu['parent_id'] in menu_map:
                # 有父菜单，添加到父菜单的children中
                parent_menu = menu_map[menu['parent_id']]
                parent_menu['children'].append(menu_item)
            else:
                # 顶级菜单
                menu_tree.append(menu_item)

        # 对菜单进行排序
        def sort_menus(menu_list):
            menu_list.sort(key=lambda x: x['sort'])
            for menu in menu_list:
                if menu['children']:
                    sort_menus(menu['children'])

        sort_menus(menu_tree)

        return success_response({
            'permissions': user_data['permissions'],
            'menus': menu_tree,
            'user_type': request.user.user_type,
            'user_info': {
                'user_id': str(request.user.user_id),
                'username': request.user.username,
                'real_name': request.user.real_name,
                'email': request.user.email,
                'user_type': request.user.user_type,
                'is_superuser': request.user.is_superuser
            }
        })
    except Exception as e:
        logger.error(f"获取用户权限失败: {str(e)}")
        return error_response('获取权限失败', code=500)
