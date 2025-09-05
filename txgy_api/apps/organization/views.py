"""
组织架构视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from utils.response import success_response, error_response
from utils.pagination import paginate_queryset
from .models import Role, Permission, Menu, RolePermission, RoleMenu, UserRole, OperationLog, SystemConfig
from .serializers import (
    RoleSerializer, PermissionSerializer, MenuSerializer, UserManagementSerializer,
    OperationLogSerializer, SystemConfigSerializer, UserPermissionSerializer,
    RoleAssignSerializer, PermissionAssignSerializer, MenuAssignSerializer
)

User = get_user_model()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def role_list(request):
    """角色列表和创建"""
    if request.method == 'GET':
        queryset = Role.objects.all().order_by('-create_time')
        
        # 搜索过滤
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(role_name__icontains=search) | Q(description__icontains=search)
            )
        
        # 分页
        page_data = paginate_queryset(queryset, request)
        serializer = RoleSerializer(page_data['results'], many=True)
        
        return success_response({
            'results': serializer.data,
            'total': page_data['total'],
            'page': page_data['page'],
            'page_size': page_data['page_size']
        })
    
    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='角色创建成功')
        return error_response('创建失败', errors=serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def role_detail(request, role_id):
    """角色详情、更新和删除"""
    try:
        role = Role.objects.get(role_id=role_id)
    except Role.DoesNotExist:
        return error_response('角色不存在', code=404)
    
    if request.method == 'GET':
        serializer = RoleSerializer(role)
        return success_response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='角色更新成功')
        return error_response('更新失败', errors=serializer.errors)
    
    elif request.method == 'DELETE':
        if role.is_default:
            return error_response('默认角色不能删除')
        
        # 检查是否有用户使用该角色
        if UserRole.objects.filter(role=role).exists():
            return error_response('该角色下还有用户，不能删除')
        
        role.delete()
        return success_response(message='角色删除成功')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def permission_list(request):
    """权限列表"""
    queryset = Permission.objects.all().order_by('module', 'function', 'action')

    print(queryset)
    
    # 按模块分组
    group_by_module = request.GET.get('group_by_module', 'false').lower() == 'true'
    if group_by_module:
        modules = {}
        for perm in queryset:
            if perm.module not in modules:
                modules[perm.module] = []
            modules[perm.module].append(PermissionSerializer(perm).data)
        return success_response(modules)
    
    serializer = PermissionSerializer(queryset, many=True)
    return success_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu_tree(request):
    """菜单树结构"""
    terminal = request.GET.get('terminal', 'pc')
    
    # 获取顶级菜单
    top_menus = Menu.objects.filter(
        parent_id__isnull=True,
        terminal=terminal,
        is_show=True
    ).order_by('sort')
    
    def build_menu_tree(menus):
        result = []
        for menu in menus:
            menu_data = MenuSerializer(menu).data
            # 获取子菜单
            children = Menu.objects.filter(
                parent_id=menu.menu_id,
                terminal=terminal,
                is_show=True
            ).order_by('sort')
            if children:
                menu_data['children'] = build_menu_tree(children)
            result.append(menu_data)
        return result
    
    menu_tree_data = build_menu_tree(top_menus)
    return success_response(menu_tree_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """获取当前用户权限和菜单"""
    user = request.user
    
    # 获取用户角色
    user_roles = UserRole.objects.filter(user=user).select_related('role')
    roles = [ur.role for ur in user_roles if ur.role.is_active]

    # 如果用户没有角色，给一个默认角色
    if not roles:
        try:
            default_role = Role.objects.filter(is_default=True, is_active=True).first()
            if default_role:
                roles = [default_role]
        except Exception:
            pass
    
    # 获取权限
    permissions = set()
    menus = set()
    
    for role in roles:
        # 角色权限
        role_perms = RolePermission.objects.filter(role=role).select_related('permission')
        permissions.update([rp.permission for rp in role_perms])
        
        # 角色菜单
        role_menus = RoleMenu.objects.filter(role=role).select_related('menu')
        menus.update([rm.menu for rm in role_menus if rm.menu.is_show])
    
    # 构建菜单树
    menu_list = list(menus)
    top_menus = [m for m in menu_list if not m.parent_id]
    
    def build_user_menu_tree(parent_menus):
        result = []
        for menu in sorted(parent_menus, key=lambda x: x.sort):
            menu_data = MenuSerializer(menu).data
            children = [m for m in menu_list if m.parent_id == menu.menu_id]
            if children:
                menu_data['children'] = build_user_menu_tree(children)
            result.append(menu_data)
        return result
    
    user_menu_tree = build_user_menu_tree(top_menus)
    
    # 序列化数据
    permissions_data = PermissionSerializer(list(permissions), many=True).data

    # 用户信息
    user_info_data = {
        'user_id': str(user.user_id),
        'username': user.username,
        'real_name': user.real_name,
        'user_type': user.user_type,
        'email': user.email
    }

    return success_response({
        'permissions': permissions_data,
        'menus': user_menu_tree,
        'user_info': user_info_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_roles(request):
    """分配角色给用户"""
    serializer = RoleAssignSerializer(data=request.data)
    if not serializer.is_valid():
        return error_response('参数错误', errors=serializer.errors)
    
    user_ids = serializer.validated_data['user_ids']
    role_ids = serializer.validated_data['role_ids']
    
    try:
        with transaction.atomic():
            # 获取用户和角色对象
            User = get_user_model()
            users = User.objects.filter(user_id__in=user_ids)
            roles = Role.objects.filter(role_id__in=role_ids)

            # 删除现有角色关联
            UserRole.objects.filter(user__in=users).delete()

            # 创建新的角色关联
            user_roles = []
            for user in users:
                for role in roles:
                    user_roles.append(UserRole(user=user, role=role))

            UserRole.objects.bulk_create(user_roles)

        return success_response(message='角色分配成功')

    except Exception as e:
        return error_response(f'角色分配失败: {str(e)}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_permissions(request):
    """分配权限给角色"""
    serializer = PermissionAssignSerializer(data=request.data)
    if not serializer.is_valid():
        return error_response('参数错误', errors=serializer.errors)
    
    role_id = serializer.validated_data['role_id']
    permission_ids = serializer.validated_data['permission_ids']
    
    try:
        with transaction.atomic():
            # 删除现有权限关联
            RolePermission.objects.filter(role_id=role_id).delete()
            
            # 创建新的权限关联
            role_permissions = []
            for perm_id in permission_ids:
                role_permissions.append(RolePermission(role_id=role_id, permission_id=perm_id))
            
            RolePermission.objects.bulk_create(role_permissions)
            
        return success_response(message='权限分配成功')
    
    except Exception as e:
        return error_response(f'权限分配失败: {str(e)}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_menus(request):
    """分配菜单给角色"""
    serializer = MenuAssignSerializer(data=request.data)
    if not serializer.is_valid():
        return error_response('参数错误', errors=serializer.errors)
    
    role_id = serializer.validated_data['role_id']
    menu_ids = serializer.validated_data['menu_ids']
    
    try:
        with transaction.atomic():
            # 删除现有菜单关联
            RoleMenu.objects.filter(role_id=role_id).delete()
            
            # 创建新的菜单关联
            role_menus = []
            for menu_id in menu_ids:
                role_menus.append(RoleMenu(role_id=role_id, menu_id=menu_id))
            
            RoleMenu.objects.bulk_create(role_menus)
            
        return success_response(message='菜单分配成功')
    
    except Exception as e:
        return error_response(f'菜单分配失败: {str(e)}')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def operation_logs(request):
    """操作日志列表"""
    queryset = OperationLog.objects.all().select_related('user').order_by('-operation_time')
    
    # 过滤条件
    user_id = request.GET.get('user_id')
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    
    module = request.GET.get('module')
    if module:
        queryset = queryset.filter(module=module)
    
    # 分页
    page_data = paginate_queryset(queryset, request)
    serializer = OperationLogSerializer(page_data['results'], many=True)
    
    return success_response({
        'results': serializer.data,
        'total': page_data['total'],
        'page': page_data['page'],
        'page_size': page_data['page_size']
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def system_configs(request):
    """系统配置列表和创建"""
    if request.method == 'GET':
        config_type = request.GET.get('type')
        queryset = SystemConfig.objects.all()
        
        if config_type:
            queryset = queryset.filter(config_type=config_type)
        
        queryset = queryset.order_by('config_type', 'config_key')
        serializer = SystemConfigSerializer(queryset, many=True)
        return success_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SystemConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='配置创建成功')
        return error_response('创建失败', errors=serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_system_config(request, config_id):
    """更新系统配置"""
    try:
        config = SystemConfig.objects.get(config_id=config_id)
    except SystemConfig.DoesNotExist:
        return error_response('配置不存在', code=404)
    
    serializer = SystemConfigSerializer(config, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_response(serializer.data, message='配置更新成功')
    return error_response('更新失败', errors=serializer.errors)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def permission_management(request):
    """权限管理 - 列表和创建"""
    if request.method == 'GET':
        # 获取权限列表
        from utils.pagination import paginate_queryset

        # 检查是否按模块分组
        group_by_module = request.GET.get('group_by_module', 'false').lower() == 'true'

        if group_by_module:
            # 按模块分组返回
            permissions = Permission.objects.all().order_by('module', 'function', 'perm_id')

            # 按模块分组
            modules = {}
            for perm in permissions:
                module_name = perm.module or '其他'
                if module_name not in modules:
                    modules[module_name] = []
                modules[module_name].append({
                    'perm_id': perm.perm_id,
                    'perm_name': perm.perm_name,
                    'perm_code': perm.perm_code,
                    'module': perm.module,
                    'function': perm.function,
                    'action': perm.action,
                    'api_path': perm.api_path,
                    'api_method': perm.api_method,
                    'description': perm.description
                })

            return success_response(modules)
        else:
            # 普通列表返回
            queryset = Permission.objects.all().order_by('module', 'function', 'perm_id')

            # 搜索过滤
            perm_name = request.GET.get('perm_name')
            if perm_name:
                queryset = queryset.filter(perm_name__icontains=perm_name)

            module = request.GET.get('module')
            if module:
                queryset = queryset.filter(module=module)

            action = request.GET.get('action')
            if action:
                queryset = queryset.filter(action=action)

            # 分页
            page_data = paginate_queryset(queryset, request)

            permissions_data = []
            for perm in page_data['results']:
                permissions_data.append({
                    'perm_id': perm.perm_id,
                    'perm_name': perm.perm_name,
                    'perm_code': perm.perm_code,
                    'module': perm.module,
                    'function': perm.function,
                    'action': perm.action,
                    'api_path': perm.api_path,
                    'api_method': perm.api_method,
                    'description': perm.description
                })

            return success_response({
                'results': permissions_data,
                'total': page_data['total'],
                'page': page_data['page'],
                'page_size': page_data['page_size']
            })

    elif request.method == 'POST':
        # 创建权限
        data = request.data

        # 检查权限代码是否已存在
        if Permission.objects.filter(perm_code=data.get('perm_code')).exists():
            return error_response('权限代码已存在')

        try:
            permission = Permission.objects.create(
                perm_name=data.get('perm_name'),
                perm_code=data.get('perm_code'),
                module=data.get('module', ''),
                function=data.get('function', ''),
                action=data.get('action', 'view'),
                api_path=data.get('api_path', ''),
                api_method=data.get('api_method', 'GET'),
                description=data.get('description', '')
            )

            return success_response({
                'perm_id': permission.perm_id,
                'perm_name': permission.perm_name,
                'perm_code': permission.perm_code,
                'module': permission.module,
                'function': permission.function,
                'action': permission.action,
                'api_path': permission.api_path,
                'api_method': permission.api_method,
                'description': permission.description
            }, message='权限创建成功')

        except Exception as e:
            return error_response(f'创建失败: {str(e)}')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def permission_detail(request, perm_id):
    """权限详情、更新和删除"""
    try:
        permission = Permission.objects.get(perm_id=perm_id)
    except Permission.DoesNotExist:
        return error_response('权限不存在', code=404)

    if request.method == 'GET':
        return success_response({
            'perm_id': permission.perm_id,
            'perm_name': permission.perm_name,
            'perm_code': permission.perm_code,
            'module': permission.module,
            'function': permission.function,
            'action': permission.action,
            'api_path': permission.api_path,
            'api_method': permission.api_method,
            'description': permission.description
        })

    elif request.method == 'PUT':
        data = request.data

        # 检查权限代码是否被其他权限使用
        if Permission.objects.filter(perm_code=data.get('perm_code')).exclude(perm_id=perm_id).exists():
            return error_response('权限代码已存在')

        try:
            permission.perm_name = data.get('perm_name', permission.perm_name)
            permission.perm_code = data.get('perm_code', permission.perm_code)
            permission.module = data.get('module', permission.module)
            permission.function = data.get('function', permission.function)
            permission.action = data.get('action', permission.action)
            permission.api_path = data.get('api_path', permission.api_path)
            permission.api_method = data.get('api_method', permission.api_method)
            permission.description = data.get('description', permission.description)
            permission.save()

            return success_response({
                'perm_id': permission.perm_id,
                'perm_name': permission.perm_name,
                'perm_code': permission.perm_code,
                'module': permission.module,
                'function': permission.function,
                'action': permission.action,
                'api_path': permission.api_path,
                'api_method': permission.api_method,
                'description': permission.description
            }, message='权限更新成功')

        except Exception as e:
            return error_response(f'更新失败: {str(e)}')

    elif request.method == 'DELETE':
        try:
            # 检查是否有角色使用此权限
            if RolePermission.objects.filter(permission=permission).exists():
                return error_response('该权限正在被角色使用，无法删除')

            permission.delete()
            return success_response(message='权限删除成功')

        except Exception as e:
            return error_response(f'删除失败: {str(e)}')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_management(request):
    """菜单管理 - 列表和创建"""
    if request.method == 'GET':
        # 获取菜单树
        terminal = request.GET.get('terminal', 'pc')
        menu_name = request.GET.get('menu_name', '')

        # 构建查询条件
        queryset = Menu.objects.filter(terminal=terminal)
        if menu_name:
            queryset = queryset.filter(menu_name__icontains=menu_name)

        # 获取所有菜单并构建树形结构
        menus = queryset.order_by('sort', 'menu_id')
        menu_tree = build_menu_tree(menus)

        return success_response(menu_tree)

    elif request.method == 'POST':
        # 创建菜单
        data = request.data

        try:
            menu = Menu.objects.create(
                parent_id=data.get('parent_id'),
                menu_name=data.get('menu_name'),
                path=data.get('path'),
                component=data.get('component', ''),
                icon=data.get('icon', ''),
                sort=data.get('sort', 0),
                terminal=data.get('terminal', 'pc'),
                is_show=data.get('is_show', True),
                is_external=data.get('is_external', False)
            )

            return success_response({
                'menu_id': menu.menu_id,
                'parent_id': menu.parent_id,
                'menu_name': menu.menu_name,
                'path': menu.path,
                'component': menu.component,
                'icon': menu.icon,
                'sort': menu.sort,
                'terminal': menu.terminal,
                'is_show': menu.is_show,
                'is_external': menu.is_external
            }, message='菜单创建成功')

        except Exception as e:
            return error_response(f'创建失败: {str(e)}')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_detail(request, menu_id):
    """菜单详情、更新和删除"""
    try:
        menu = Menu.objects.get(menu_id=menu_id)
    except Menu.DoesNotExist:
        return error_response('菜单不存在', code=404)

    if request.method == 'GET':
        return success_response({
            'menu_id': menu.menu_id,
            'parent_id': menu.parent_id,
            'menu_name': menu.menu_name,
            'path': menu.path,
            'component': menu.component,
            'icon': menu.icon,
            'sort': menu.sort,
            'terminal': menu.terminal,
            'is_show': menu.is_show,
            'is_external': menu.is_external
        })

    elif request.method == 'PUT':
        data = request.data

        try:
            # 检查是否会形成循环引用
            parent_id = data.get('parent_id')
            if parent_id and is_circular_reference(menu_id, parent_id):
                return error_response('不能将菜单设置为自己或子菜单的父菜单')

            menu.parent_id = parent_id
            menu.menu_name = data.get('menu_name', menu.menu_name)
            menu.path = data.get('path', menu.path)
            menu.component = data.get('component', menu.component)
            menu.icon = data.get('icon', menu.icon)
            menu.sort = data.get('sort', menu.sort)
            menu.terminal = data.get('terminal', menu.terminal)
            menu.is_show = data.get('is_show', menu.is_show)
            menu.is_external = data.get('is_external', menu.is_external)
            menu.save()

            return success_response({
                'menu_id': menu.menu_id,
                'parent_id': menu.parent_id,
                'menu_name': menu.menu_name,
                'path': menu.path,
                'component': menu.component,
                'icon': menu.icon,
                'sort': menu.sort,
                'terminal': menu.terminal,
                'is_show': menu.is_show,
                'is_external': menu.is_external
            }, message='菜单更新成功')

        except Exception as e:
            return error_response(f'更新失败: {str(e)}')

    elif request.method == 'DELETE':
        try:
            force_delete = request.GET.get('force', 'false').lower() == 'true'

            if not force_delete:
                # 常规删除检查
                if Menu.objects.filter(parent_id=menu_id).exists():
                    return error_response('该菜单下还有子菜单，请先删除子菜单')

                if RoleMenu.objects.filter(menu=menu).exists():
                    return error_response('该菜单正在被角色使用，无法删除')
            else:
                # 强制删除：先移除角色关联，再递归删除子菜单
                def delete_menu_recursive(menu_obj):
                    # 递归删除子菜单
                    children = Menu.objects.filter(parent_id=menu_obj.menu_id)
                    for child in children:
                        delete_menu_recursive(child)

                    # 删除角色菜单关联
                    RoleMenu.objects.filter(menu=menu_obj).delete()
                    # 删除菜单
                    menu_obj.delete()

                delete_menu_recursive(menu)
                return success_response(message='菜单强制删除成功')

            menu.delete()
            return success_response(message='菜单删除成功')

        except Exception as e:
            return error_response(f'删除失败: {str(e)}')


def build_menu_tree(menus):
    """构建菜单树形结构"""
    menu_dict = {}
    menu_tree = []

    # 先将所有菜单转换为字典
    for menu in menus:
        menu_dict[menu.menu_id] = {
            'menu_id': menu.menu_id,
            'parent_id': menu.parent_id,
            'menu_name': menu.menu_name,
            'path': menu.path,
            'component': menu.component,
            'icon': menu.icon,
            'sort': menu.sort,
            'terminal': menu.terminal,
            'is_show': menu.is_show,
            'is_external': menu.is_external,
            'children': []
        }

    # 构建树形结构
    for menu in menus:
        menu_data = menu_dict[menu.menu_id]
        if menu.parent_id and menu.parent_id in menu_dict:
            # 有父菜单，添加到父菜单的children中
            menu_dict[menu.parent_id]['children'].append(menu_data)
        else:
            # 顶级菜单
            menu_tree.append(menu_data)

    return menu_tree


def is_circular_reference(menu_id, parent_id):
    """检查是否会形成循环引用"""
    if menu_id == parent_id:
        return True

    # 递归检查父菜单链
    try:
        parent_menu = Menu.objects.get(menu_id=parent_id)
        if parent_menu.parent_id:
            return is_circular_reference(menu_id, parent_menu.parent_id)
    except Menu.DoesNotExist:
        pass

    return False
