"""
自定义权限类
"""
from rest_framework.permissions import BasePermission


class IsEnterpriseUser(BasePermission):
    """企业用户权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type == 'enterprise'
        )


class IsIndividualUser(BasePermission):
    """个人用户权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.user_type == 'individual'
        )


class IsSupplier(BasePermission):
    """供应商权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'enterprise' and
            hasattr(request.user, 'enterprise') and
            request.user.enterprise.company_type == 'supplier'
        )


class IsManufacturer(BasePermission):
    """生产制造企业权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'enterprise' and
            hasattr(request.user, 'enterprise') and
            request.user.enterprise.company_type == 'manufacturer'
        )


class IsConstructor(BasePermission):
    """施工安装企业权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'enterprise' and
            hasattr(request.user, 'enterprise') and
            request.user.enterprise.company_type == 'constructor'
        )


class IsOwner(BasePermission):
    """工程甲方企业权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'enterprise' and
            hasattr(request.user, 'enterprise') and
            request.user.enterprise.company_type == 'owner'
        )


class IsOwnerOrReadOnly(BasePermission):
    """所有者权限或只读"""
    
    def has_object_permission(self, request, view, obj):
        # 读权限对所有人开放
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # 写权限只对所有者开放
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False


class IsVerifiedEnterprise(BasePermission):
    """已认证企业权限"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'enterprise' and
            hasattr(request.user, 'enterprise') and
            request.user.enterprise.certification_status == 'verified'
        )
