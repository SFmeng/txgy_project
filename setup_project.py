#!/usr/bin/env python
"""
项目基础架构初始化脚本
"""
import os
import sys

def create_app_structure():
    """创建应用模块基础结构"""
    
    apps = [
        'search_match',
        'communication', 
        'resources',
        'business',
        'tech_service',
        'bidding',
        'data_center'
    ]
    
    for app in apps:
        app_dir = f'txgy_api/apps/{app}'
        
        # 创建应用目录
        os.makedirs(app_dir, exist_ok=True)
        
        # 创建基础文件
        files = {
            '__init__.py': f'# {app}模块',
            'apps.py': f'''from django.apps import AppConfig


class {app.title().replace('_', '')}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
    verbose_name = '{get_app_verbose_name(app)}'
''',
            'models.py': f'''"""
{get_app_verbose_name(app)}模型
"""
from django.db import models
from apps.common.models import BaseModel

# TODO: 添加{get_app_verbose_name(app)}相关模型
''',
            'views.py': f'''"""
{get_app_verbose_name(app)}视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from utils.response import success_response, error_response

# TODO: 添加{get_app_verbose_name(app)}相关视图
''',
            'serializers.py': f'''"""
{get_app_verbose_name(app)}序列化器
"""
from rest_framework import serializers

# TODO: 添加{get_app_verbose_name(app)}相关序列化器
''',
            'urls.py': f'''"""
{get_app_verbose_name(app)}URL配置
"""
from django.urls import path
from . import views

app_name = '{app}'

urlpatterns = [
    # TODO: 添加{get_app_verbose_name(app)}相关URL
]
''',
            'admin.py': f'''"""
{get_app_verbose_name(app)}管理后台
"""
from django.contrib import admin

# TODO: 添加{get_app_verbose_name(app)}相关管理后台配置
''',
        }
        
        for filename, content in files.items():
            filepath = os.path.join(app_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        print(f"✓ 创建应用模块: {app}")

def get_app_verbose_name(app):
    """获取应用中文名称"""
    names = {
        'search_match': '搜索匹配',
        'communication': '沟通交流',
        'resources': '资源管理',
        'business': '商务服务',
        'tech_service': '技术服务',
        'bidding': '招投标',
        'data_center': '数据中心'
    }
    return names.get(app, app)

def create_frontend_structure():
    """创建前端基础结构"""
    
    # 创建前端目录结构
    dirs = [
        'txgy_frontend/src/api',
        'txgy_frontend/src/components/common',
        'txgy_frontend/src/components/business',
        'txgy_frontend/src/components/layout',
        'txgy_frontend/src/composables',
        'txgy_frontend/src/layouts',
        'txgy_frontend/src/pages/auth',
        'txgy_frontend/src/pages/dashboard',
        'txgy_frontend/src/pages/products',
        'txgy_frontend/src/pages/search',
        'txgy_frontend/src/pages/communication',
        'txgy_frontend/src/pages/profile',
        'txgy_frontend/src/router/modules',
        'txgy_frontend/src/stores',
        'txgy_frontend/src/utils',
        'txgy_frontend/src/assets/images',
        'txgy_frontend/src/assets/icons',
        'txgy_frontend/public'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        
        # 创建.gitkeep文件保持目录结构
        gitkeep_path = os.path.join(dir_path, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')
    
    print("✓ 创建前端目录结构")

def create_backend_structure():
    """创建后端基础结构"""
    
    # 创建后端目录结构
    dirs = [
        'txgy_api/logs',
        'txgy_api/media/avatars',
        'txgy_api/media/uploads',
        'txgy_api/static',
        'txgy_api/staticfiles',
        'txgy_api/templates',
        'txgy_api/fixtures',
        'txgy_api/tests'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        
        # 创建.gitkeep文件保持目录结构
        gitkeep_path = os.path.join(dir_path, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')
    
    print("✓ 创建后端目录结构")

def create_config_files():
    """创建配置文件"""
    
    # 创建.gitignore文件
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment variables
.env
.env.local
.env.development
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# Build outputs
dist/
build/

# Logs
logs/
*.log

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
.nyc_output

# Dependency directories
node_modules/
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
'''
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✓ 创建.gitignore文件")

def create_readme_files():
    """创建README文件"""
    
    # 创建项目启动说明
    startup_content = '''# 防腐保温智慧平台 - 快速启动指南

## 后端启动

1. 进入后端目录：
```bash
cd txgy_api
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

3. 安装依赖：
```bash
pip install -r requirements/development.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件，配置数据库等信息
```

5. 数据库迁移：
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. 启动开发服务器：
```bash
python manage.py runserver 0.0.0.0:8000
```

## 前端启动

1. 进入前端目录：
```bash
cd txgy_frontend
```

2. 安装依赖：
```bash
npm install
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件
```

4. 启动开发服务器：
```bash
npm run dev
```

## 访问地址

- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/swagger/
- 管理后台：http://localhost:8000/admin/

## 项目结构

```
pipe_project/
├── txgy_frontend/          # 前端项目
├── txgy_api/              # 后端项目
├── docs/                  # 项目文档
└── README.md             # 项目说明
```

## 开发规范

请参考 `docs/开发规范文档.md` 了解详细的开发规范。
'''
    
    with open('STARTUP.md', 'w', encoding='utf-8') as f:
        f.write(startup_content)
    
    print("✓ 创建启动指南")

def main():
    """主函数"""
    print("🚀 开始初始化防腐保温智慧平台基础架构...")
    
    try:
        create_app_structure()
        create_frontend_structure()
        create_backend_structure()
        create_config_files()
        create_readme_files()
        
        print("\n✅ 项目基础架构初始化完成！")
        print("\n📋 下一步操作：")
        print("1. 配置数据库连接信息")
        print("2. 安装项目依赖")
        print("3. 执行数据库迁移")
        print("4. 启动开发服务器")
        print("\n详细说明请查看 STARTUP.md 文件")
        
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
