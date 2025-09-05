# 防腐保温智慧平台 - 快速启动指南

## 后端启动

1. 进入后端目录：
```bash
cd txgy_api
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
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
