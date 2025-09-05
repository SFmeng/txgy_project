# 防腐保温智慧平台

## 项目简介

防腐保温智慧平台是一个专为防腐保温行业打造的综合性信息交互与资源整合平台。平台通过信息发布、搜索匹配、沟通互动等核心功能，连接生产制造企业、施工安装企业、工程甲方企业、供应商企业以及行业专业人士，实现高效的信息交流和商务合作。

## 核心功能

### 🏢 企业服务
- **生产制造企业**: 产品推广、原材料采购、代理商拓展、人才招聘
- **施工安装企业**: 项目对接、材料采购、案例展示、成本核算
- **工程甲方企业**: 招标发布、供应商筛选、项目管控、成本审核
- **供应商企业**: 产品展示、需求响应、订单管理、客户维护

### 👥 个人服务
- **技术人员/工程师**: 就业对接、技术学习、难题咨询、服务变现
- **施工人员**: 工作匹配、技能展示、薪资参考
- **行业专家**: 技术咨询、观点发布、合作对接
- **采购人员**: 供应商筛选、产品比价、招投标跟踪

### 🔧 平台功能
- **信息发布系统**: 多类型信息发布、审核、推送
- **搜索匹配系统**: 多维度搜索、智能推荐、自动匹配
- **沟通互动系统**: 即时通讯、报价议价、视频会议
- **资源整合中心**: 供应商库、项目库、人才库、资料库
- **商务服务平台**: 交易管理、库存管理、成本核算
- **智能技术服务**: AI问答、专家咨询、技术案例
- **招投标平台**: 招标发布、投标管理、标书生成

## 技术架构

### 前端技术栈
- **框架**: Vue 3.4+ (组合式API)
- **路由**: Vue Router 4.x
- **状态管理**: Pinia 2.x
- **HTTP客户端**: Axios 1.x
- **UI组件**: Element Plus 2.x
- **CSS框架**: Tailwind CSS 3.x
- **构建工具**: Vite 5.x

### 后端技术栈
- **语言**: Python 3.12.3
- **框架**: Django 5.2.5
- **API框架**: Django REST Framework 3.15+
- **数据库**: MySQL 8.0+ (主数据库)
- **缓存**: Redis 6.0+
- **搜索**: Elasticsearch 8.0+
- **任务队列**: Celery 5.3+
- **Web服务器**: Nginx + Gunicorn

## 项目结构

```
pipe_project/
├── txgy_frontend/              # 前端项目
│   ├── src/
│   │   ├── api/               # API接口封装
│   │   ├── components/        # 公共组件
│   │   ├── pages/             # 页面组件
│   │   ├── stores/            # 状态管理
│   │   ├── router/            # 路由配置
│   │   └── utils/             # 工具函数
│   ├── package.json
│   └── vite.config.js
├── txgy_api/                   # 后端项目
│   ├── config/                # 项目配置
│   ├── apps/                  # 应用模块
│   │   ├── authentication/    # 用户认证
│   │   ├── info_publish/      # 信息发布
│   │   ├── search_match/      # 搜索匹配
│   │   ├── communication/     # 沟通交流
│   │   ├── resources/         # 资源管理
│   │   ├── business/          # 商务服务
│   │   ├── tech_service/      # 技术服务
│   │   └── bidding/           # 招投标
│   ├── utils/                 # 工具函数
│   ├── requirements/          # 依赖文件
│   └── manage.py
└── docs/                       # 项目文档
    ├── API接口文档.md
    ├── 数据库设计文档.md
    ├── 前端开发文档.md
    ├── 后端开发文档.md
    ├── 部署文档.md
    └── 开发规范文档.md
```

## 快速开始

### 环境要求
- Python 3.12+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+
- Elasticsearch 8.0+

### 后端启动
```bash
# 进入后端目录
cd txgy_api

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements/development.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库等信息

# 数据库迁移
python manage.py migrate

# 加载初始数据
python manage.py loaddata fixtures/initial_data.json

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 前端启动
```bash
# 进入前端目录
cd txgy_frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 启动其他服务
```bash
# 启动Redis (如果未启动)
redis-server

# 启动Elasticsearch (如果未启动)
elasticsearch

# 启动Celery Worker (后台任务)
cd txgy_api
celery -A config worker -l info

# 启动Celery Beat (定时任务)
celery -A config beat -l info
```

## 开发指南

### API文档
- 在线API文档: http://localhost:8000/swagger/
- 详细接口文档: [docs/API接口文档.md](docs/API接口文档.md)

### 数据库设计
- 数据库设计文档: [docs/数据库设计文档.md](docs/数据库设计文档.md)
- ER图: [docs/数据库ER图.png](docs/数据库ER图.png)

### 开发规范
- 代码规范: [docs/开发规范文档.md](docs/开发规范文档.md)
- 前端开发指南: [docs/前端开发文档.md](docs/前端开发文档.md)
- 后端开发指南: [docs/后端开发文档.md](docs/后端开发文档.md)

## 部署指南

详细部署说明请参考: [docs/部署文档.md](docs/部署文档.md)

### 生产环境部署
1. 服务器环境准备
2. 数据库安装配置
3. 应用代码部署
4. Web服务器配置
5. 监控和日志配置

## 测试

### 运行测试
```bash
# 后端测试
cd txgy_api
python manage.py test

# 前端测试
cd txgy_frontend
npm run test
```

### 测试覆盖率
```bash
# 后端测试覆盖率
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# 前端测试覆盖率
npm run test:coverage
```

## 贡献指南

### 开发流程
1. Fork 项目到个人仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加某个功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范
- 遵循项目代码规范
- 添加必要的测试用例
- 更新相关文档
- 通过所有自动化检查

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者: 开发团队
- 邮箱: dev@txgy-platform.com
- 技术支持: support@txgy-platform.com

## 更新日志

### v1.0.0 (2024-08-27)
- 初始版本发布
- 实现核心功能模块
- 完成基础架构搭建

### 开发计划
- [ ] 用户认证与权限管理
- [ ] 信息发布系统
- [ ] 搜索匹配系统
- [ ] 沟通互动系统
- [ ] 资源整合中心
- [ ] 商务服务平台
- [ ] 智能技术服务
- [ ] 招投标平台
- [ ] 数据中心
- [ ] 移动端适配
- [ ] 性能优化
- [ ] 安全加固

## 常见问题

### Q: 如何重置管理员密码？
A: 使用命令 `python manage.py changepassword admin`

### Q: 如何清理缓存？
A: 使用命令 `python manage.py shell` 然后执行 `from django.core.cache import cache; cache.clear()`

### Q: 如何重建搜索索引？
A: 使用命令 `python manage.py rebuild_index`

### Q: 前端开发时API跨域问题？
A: 确保后端CORS配置正确，或使用Vite代理配置

---

**注意**: 这是一个企业级应用，请确保在生产环境中正确配置安全设置，包括但不限于HTTPS、防火墙、数据加密等。
# tianxin_shixun
