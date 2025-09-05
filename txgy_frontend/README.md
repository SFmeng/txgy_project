# 防腐保温智慧平台 - 前端项目

## 项目简介
基于Vue 3 + Element Plus构建的防腐保温行业信息交互平台前端应用。

## 技术栈
- Vue 3.4+ (Composition API)
- Vue Router 4.x
- Pinia 2.x
- Element Plus 2.x
- Tailwind CSS 3.x
- Axios 1.x
- Vite 5.x

## 快速开始

### 环境要求
- Node.js 18.0+
- npm 9.0+ / yarn 1.22+ / pnpm 8.0+

### 安装依赖
```bash
npm install
```

### 开发环境启动
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 代码检查和格式化
```bash
npm run lint
npm run format
```

### 运行测试
```bash
npm run test
npm run test:coverage
```

## 项目结构
```
src/
├── api/                    # API接口封装
│   ├── auth.js            # 认证相关接口
│   ├── products.js        # 产品相关接口
│   ├── search.js          # 搜索相关接口
│   └── index.js           # 接口统一导出
├── assets/                 # 静态资源
│   ├── images/            # 图片资源
│   ├── icons/             # 图标资源
│   └── styles/            # 全局样式
├── components/             # 公共组件
│   ├── common/            # 通用组件
│   ├── business/          # 业务组件
│   └── layout/            # 布局组件
├── composables/            # 组合式函数
│   ├── useAuth.js         # 认证相关
│   ├── useSearch.js       # 搜索相关
│   └── useWebSocket.js    # WebSocket相关
├── layouts/                # 布局组件
│   ├── DefaultLayout.vue  # 默认布局
│   ├── AuthLayout.vue     # 认证页面布局
│   └── AdminLayout.vue    # 管理后台布局
├── pages/                  # 页面组件
│   ├── auth/              # 认证页面
│   ├── dashboard/         # 仪表板
│   ├── products/          # 产品相关页面
│   ├── search/            # 搜索页面
│   ├── communication/     # 沟通交流页面
│   └── profile/           # 用户资料页面
├── router/                 # 路由配置
│   ├── index.js           # 主路由文件
│   ├── guards.js          # 路由守卫
│   └── modules/           # 模块化路由
├── stores/                 # Pinia状态管理
│   ├── auth.js            # 认证状态
│   ├── user.js            # 用户信息状态
│   ├── products.js        # 产品状态
│   └── index.js           # 状态管理入口
├── utils/                  # 工具函数
│   ├── request.js         # HTTP请求封装
│   ├── auth.js            # 认证工具
│   ├── validation.js      # 数据验证
│   ├── format.js          # 数据格式化
│   └── constants.js       # 常量定义
├── App.vue                 # 根组件
└── main.js                 # 应用入口
```

## 开发规范
详细的开发规范请参考：[../docs/开发规范文档.md](../docs/开发规范文档.md)

## API文档
接口文档请参考：[../docs/API接口文档.md](../docs/API接口文档.md)
