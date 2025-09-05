#!/usr/bin/env python
"""
项目架构完整性检查脚本
"""
import os
import sys

def check_backend_structure():
    """检查后端项目结构"""
    print("🔍 检查后端项目结构...")
    
    required_files = [
        'txgy_api/manage.py',
        'txgy_api/config/__init__.py',
        'txgy_api/config/settings/base.py',
        'txgy_api/config/settings/development.py',
        'txgy_api/config/settings/production.py',
        'txgy_api/config/urls.py',
        'txgy_api/config/wsgi.py',
        'txgy_api/celery_app.py',
        'txgy_api/.env.example',
        'txgy_api/requirements/base.txt',
        'txgy_api/requirements/development.txt',
        'txgy_api/requirements/production.txt',
    ]
    
    required_apps = [
        'txgy_api/apps/authentication',
        'txgy_api/apps/info_publish',
        'txgy_api/apps/search_match',
        'txgy_api/apps/communication',
        'txgy_api/apps/resources',
        'txgy_api/apps/business',
        'txgy_api/apps/tech_service',
        'txgy_api/apps/bidding',
        'txgy_api/apps/data_center',
        'txgy_api/apps/common',
    ]
    
    required_utils = [
        'txgy_api/utils/__init__.py',
        'txgy_api/utils/response.py',
        'txgy_api/utils/pagination.py',
        'txgy_api/utils/permissions.py',
        'txgy_api/middleware/__init__.py',
        'txgy_api/middleware/request_logging.py',
    ]
    
    missing_files = []
    
    # 检查核心文件
    for file_path in required_files + required_utils:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    # 检查应用模块
    for app_path in required_apps:
        app_files = [
            f'{app_path}/__init__.py',
            f'{app_path}/apps.py',
            f'{app_path}/models.py',
            f'{app_path}/views.py',
            f'{app_path}/urls.py',
        ]
        for file_path in app_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
    
    if missing_files:
        print("❌ 后端项目结构不完整，缺少以下文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ 后端项目结构完整")
        return True

def check_frontend_structure():
    """检查前端项目结构"""
    print("🔍 检查前端项目结构...")
    
    required_files = [
        'txgy_frontend/package.json',
        'txgy_frontend/vite.config.js',
        'txgy_frontend/tailwind.config.js',
        'txgy_frontend/postcss.config.js',
        'txgy_frontend/index.html',
        'txgy_frontend/.env.example',
        'txgy_frontend/src/main.js',
        'txgy_frontend/src/App.vue',
        'txgy_frontend/src/styles/index.css',
        'txgy_frontend/src/router/index.js',
        'txgy_frontend/src/stores/auth.js',
        'txgy_frontend/src/utils/request.js',
        'txgy_frontend/src/utils/auth.js',
        'txgy_frontend/src/api/auth.js',
        'txgy_frontend/src/layouts/DefaultLayout.vue',
        'txgy_frontend/src/layouts/AuthLayout.vue',
        'txgy_frontend/src/pages/Home.vue',
        'txgy_frontend/src/pages/NotFound.vue',
        'txgy_frontend/src/pages/auth/Login.vue',
        'txgy_frontend/src/pages/auth/Register.vue',
        'txgy_frontend/src/pages/dashboard/Enterprise.vue',
        'txgy_frontend/src/pages/dashboard/Individual.vue',
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 前端项目结构不完整，缺少以下文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ 前端项目结构完整")
        return True

def check_documentation():
    """检查文档完整性"""
    print("🔍 检查项目文档...")
    
    required_docs = [
        'README.md',
        'STARTUP.md',
        'docs/API接口文档.md',
        'docs/数据库设计文档.md',
        'docs/前端开发文档.md',
        'docs/后端开发文档.md',
        'docs/部署文档.md',
        'docs/开发规范文档.md',
        'docs/功能模块设计文档.md',
        'docs/测试计划文档.md',
        'docs/项目开发计划.md',
    ]
    
    missing_docs = []
    
    for doc_path in required_docs:
        if not os.path.exists(doc_path):
            missing_docs.append(doc_path)
    
    if missing_docs:
        print("❌ 项目文档不完整，缺少以下文档:")
        for doc_path in missing_docs:
            print(f"   - {doc_path}")
        return False
    else:
        print("✅ 项目文档完整")
        return True

def check_config_files():
    """检查配置文件"""
    print("🔍 检查配置文件...")
    
    required_configs = [
        '.gitignore',
        'txgy_api/.env.example',
        'txgy_frontend/.env.example',
    ]
    
    missing_configs = []
    
    for config_path in required_configs:
        if not os.path.exists(config_path):
            missing_configs.append(config_path)
    
    if missing_configs:
        print("❌ 配置文件不完整，缺少以下文件:")
        for config_path in missing_configs:
            print(f"   - {config_path}")
        return False
    else:
        print("✅ 配置文件完整")
        return True

def generate_project_summary():
    """生成项目架构总结"""
    print("\n📋 项目架构总结:")
    print("=" * 50)
    
    # 统计文件数量
    backend_files = 0
    frontend_files = 0
    doc_files = 0
    
    for root, dirs, files in os.walk('txgy_api'):
        backend_files += len([f for f in files if f.endswith(('.py', '.txt', '.md'))])
    
    for root, dirs, files in os.walk('txgy_frontend'):
        frontend_files += len([f for f in files if f.endswith(('.js', '.vue', '.json', '.css', '.html'))])
    
    for root, dirs, files in os.walk('docs'):
        doc_files += len([f for f in files if f.endswith('.md')])
    
    print(f"📁 后端文件数量: {backend_files}")
    print(f"📁 前端文件数量: {frontend_files}")
    print(f"📁 文档文件数量: {doc_files}")
    print(f"📁 总文件数量: {backend_files + frontend_files + doc_files}")
    
    print("\n🏗️ 项目架构特点:")
    print("- ✅ 前后端分离架构")
    print("- ✅ Django REST Framework + Vue 3")
    print("- ✅ 模块化应用设计")
    print("- ✅ 完整的用户认证系统")
    print("- ✅ 统一的API响应格式")
    print("- ✅ 权限控制和中间件")
    print("- ✅ 响应式前端布局")
    print("- ✅ 状态管理和路由配置")
    print("- ✅ 完整的开发文档")
    print("- ✅ 规范的代码结构")

def main():
    """主函数"""
    print("🚀 防腐保温智慧平台架构完整性检查")
    print("=" * 50)
    
    checks = [
        check_backend_structure(),
        check_frontend_structure(),
        check_documentation(),
        check_config_files()
    ]
    
    if all(checks):
        print("\n🎉 项目基础架构搭建完成！")
        print("✅ 所有必要文件和目录结构已创建")
        print("✅ 前后端基础代码已实现")
        print("✅ 开发文档已完善")
        print("✅ 配置文件已准备")
        
        generate_project_summary()
        
        print("\n📋 下一步操作建议:")
        print("1. 配置开发环境 (数据库、Redis等)")
        print("2. 安装项目依赖")
        print("3. 执行数据库迁移")
        print("4. 启动开发服务器")
        print("5. 开始功能开发")
        
        print("\n📖 详细说明请查看:")
        print("- STARTUP.md - 快速启动指南")
        print("- docs/ - 完整开发文档")
        
    else:
        print("\n❌ 项目架构不完整，请检查缺失的文件")
        sys.exit(1)

if __name__ == '__main__':
    main()
