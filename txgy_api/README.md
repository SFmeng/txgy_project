# 防腐保温智慧平台 - 后端API

## 项目简介
基于Django + Django REST Framework构建的防腐保温行业信息交互平台后端API服务。

## 技术栈
- Python 3.12.3
- Django 5.2.5
- Django REST Framework 3.15+
- MySQL 8.0+ (主数据库)
- Redis 6.0+ (缓存)
- Elasticsearch 8.0+ (搜索)
- Celery 5.3+ (任务队列)

## 快速开始

### 环境要求
- Python 3.12+
- MySQL 8.0+
- Redis 6.0+
- Elasticsearch 8.0+

### 安装依赖
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements/development.txt
```

### 环境配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

### 数据库初始化
```bash
# 执行数据库迁移
python manage.py migrate

# 加载初始数据
python manage.py loaddata fixtures/initial_data.json

# 创建超级用户
python manage.py createsuperuser
```

### 启动服务
```bash
# 启动Django开发服务器
python manage.py runserver 0.0.0.0:8000

# 启动Celery Worker (新终端)
celery -A config worker -l info

# 启动Celery Beat (新终端)
celery -A config beat -l info
```

## 项目结构
```
txgy_api/
├── config/                     # 项目配置
│   ├── settings/              # 分环境配置
│   │   ├── base.py           # 基础配置
│   │   ├── development.py    # 开发环境
│   │   ├── production.py     # 生产环境
│   │   └── testing.py        # 测试环境
│   ├── urls.py               # 主路由配置
│   └── wsgi.py               # WSGI配置
├── apps/                      # 应用模块
│   ├── authentication/       # 用户认证模块
│   │   ├── models.py         # 数据模型
│   │   ├── views.py          # 视图函数
│   │   ├── serializers.py    # 序列化器
│   │   ├── urls.py           # 路由配置
│   │   └── tests/            # 测试用例
│   ├── info_publish/         # 信息发布模块
│   ├── search_match/         # 搜索匹配模块
│   ├── communication/        # 沟通交流模块
│   ├── resources/            # 资源管理模块
│   ├── business/             # 商务服务模块
│   ├── tech_service/         # 技术服务模块
│   ├── bidding/              # 招投标模块
│   ├── data_center/          # 数据中心模块
│   └── common/               # 公共模块
├── utils/                     # 工具函数
│   ├── response.py           # 响应格式化
│   ├── pagination.py         # 分页工具
│   ├── permissions.py        # 权限工具
│   ├── encryption.py         # 加密工具
│   └── validators.py         # 验证器
├── middleware/                # 中间件
│   ├── request_logging.py    # 请求日志
│   ├── rate_limiting.py      # 限流中间件
│   └── security.py           # 安全中间件
├── fixtures/                  # 初始数据
├── logs/                      # 日志文件
├── media/                     # 媒体文件
├── static/                    # 静态文件
├── requirements/              # 依赖文件
├── manage.py                  # Django管理脚本
└── celery_app.py             # Celery配置
```

## API文档
- 在线API文档: http://localhost:8000/swagger/
- 详细接口文档: [../docs/API接口文档.md](../docs/API接口文档.md)

## 数据库设计
数据库设计文档: [../docs/数据库设计文档.md](../docs/数据库设计文档.md)

## 开发规范
开发规范文档: [../docs/开发规范文档.md](../docs/开发规范文档.md)

## 测试
```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test apps.authentication

# 生成测试覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 部署
部署文档: [../docs/部署文档.md](../docs/部署文档.md)
