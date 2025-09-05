#!/usr/bin/env python
"""
部署状态检查脚本
"""
import requests
import time
import sys

def check_backend_status():
    """检查后端服务状态"""
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务运行正常 (端口8000)")
            return True
        else:
            print(f"❌ 后端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 后端服务连接失败: {str(e)}")
        return False

def check_frontend_status():
    """检查前端服务状态"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务运行正常 (端口3000)")
            return True
        else:
            print(f"❌ 前端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 前端服务连接失败: {str(e)}")
        return False

def check_database_connection():
    """检查数据库连接"""
    try:
        import os
        import django
        
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
        sys.path.append('txgy_api')
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ 数据库连接正常")
            return True
        else:
            print("❌ 数据库连接异常")
            return False
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 防腐保温智慧平台部署状态检查")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(3)
    
    checks = []
    
    # 检查数据库连接
    print("\n🔍 检查数据库连接...")
    checks.append(check_database_connection())
    
    # 检查后端服务
    print("\n🔍 检查后端服务...")
    checks.append(check_backend_status())
    
    # 检查前端服务
    print("\n🔍 检查前端服务...")
    checks.append(check_frontend_status())
    
    # 总结
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 项目部署成功！")
        print("\n📋 访问地址:")
        print("- 前端应用: http://localhost:3000")
        print("- 后端API: http://localhost:8000")
        print("- 管理后台: http://localhost:8000/admin/")
        print("- API文档: http://localhost:8000/swagger/")
        
        print("\n🔑 管理员账号:")
        print("- 用户名: admin")
        print("- 密码: admin123456")
        print("- 邮箱: admin@txgy.com")
        
        print("\n💾 数据库信息:")
        print("- 数据库: txgy_platform")
        print("- 用户名: root")
        print("- 端口: 3306")
        
        print("\n✨ 部署完成，可以开始使用了！")
    else:
        print("❌ 部署存在问题，请检查服务状态")
        failed_count = len([c for c in checks if not c])
        print(f"失败检查项: {failed_count}/{len(checks)}")

if __name__ == '__main__':
    main()
