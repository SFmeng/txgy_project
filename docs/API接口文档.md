# 防腐保温智慧平台 API 接口文档

## 文档概述

本文档基于《防腐保温智慧平台需求分析文档》，详细定义了系统各模块的API接口规范，包括请求参数、响应格式、错误处理等。

### 技术架构
- **前端**: Vue3 + VueRouter + Pinia + Axios + ElementPlus + TailwindCSS
- **后端**: Python 3.12.3 + Django 5.2.5 + Django REST Framework
- **数据库**: MySQL 8.0+ (主数据库) + Redis 6.0+ (缓存) + Elasticsearch 8.0+ (搜索)

### 接口规范
- **协议**: HTTPS
- **数据格式**: JSON
- **认证方式**: JWT Token
- **编码**: UTF-8

## 通用接口规范

### 请求头
```http
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
Accept: application/json
```

### 通用响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-08-27T10:30:00Z",
  "request_id": "req_123456789"
}
```

### 状态码说明
- `200`: 成功
- `400`: 请求参数错误
- `401`: 未授权/Token无效
- `403`: 权限不足
- `404`: 资源不存在
- `422`: 数据验证失败
- `500`: 服务器内部错误

### 分页参数
```json
{
  "page": 1,
  "page_size": 10,
  "total": 100,
  "total_pages": 10
}
```

## 1. 用户认证与权限管理模块

### 1.1 用户注册

**接口地址**: `POST /api/v1/auth/register`

**请求参数**:
```json
{
  "username": "string(50)",          // 用户名，唯一
  "password": "string(8-20)",        // 密码，包含字母数字
  "email": "string",                 // 邮箱地址
  "phone": "string(11)",             // 手机号码
  "user_type": "string",             // 用户类型: enterprise/individual
  "real_name": "string(50)",         // 真实姓名
  "enterprise_info": {               // 企业用户必填
    "company_name": "string(100)",   // 企业名称
    "company_type": "string",        // 企业类型: manufacturer/constructor/owner/supplier
    "business_license": "string",    // 营业执照号
    "contact_person": "string(50)",  // 联系人
    "address": "string(200)"         // 企业地址
  },
  "verification_code": "string(6)"   // 短信验证码
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user_id": "USR-202408-001",
    "username": "test_user",
    "user_type": "enterprise",
    "status": "pending_review"  // 待审核状态
  }
}
```

### 1.2 用户登录

**接口地址**: `POST /api/v1/auth/login`

**请求参数**:
```json
{
  "username": "string",     // 用户名或手机号
  "password": "string",     // 密码
  "login_type": "string"    // 登录方式: password/sms
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 3600,
    "user_info": {
      "user_id": "USR-202408-001",
      "username": "test_user",
      "user_type": "enterprise",
      "permissions": ["info_publish", "search_match", "communication"],
      "enterprise_info": {
        "company_name": "测试企业",
        "company_type": "manufacturer"
      }
    }
  }
}
```

### 1.3 Token刷新

**接口地址**: `POST /api/v1/auth/refresh`

**请求参数**:
```json
{
  "refresh_token": "string"
}
```

### 1.4 用户信息获取

**接口地址**: `GET /api/v1/auth/profile`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": "USR-202408-001",
    "username": "test_user",
    "email": "test@example.com",
    "phone": "13800138000",
    "user_type": "enterprise",
    "real_name": "张三",
    "avatar": "https://example.com/avatar.jpg",
    "enterprise_info": {
      "company_name": "测试企业有限公司",
      "company_type": "manufacturer",
      "business_license": "91110000123456789X",
      "contact_person": "张三",
      "address": "北京市朝阳区测试路123号"
    },
    "created_at": "2024-08-01T10:00:00Z",
    "last_login": "2024-08-27T10:30:00Z"
  }
}
```

## 2. 信息发布系统模块

### 2.1 供应信息发布

**接口地址**: `POST /api/v1/info/supply`

**请求参数**:
```json
{
  "product_name": "string(50)",           // 产品名称，必填
  "product_type": "string",               // 产品类型，关联产品分类字典
  "technical_params": {                   // 技术参数，JSON格式
    "temperature_range": "string",        // 耐温范围
    "corrosion_level": "string",          // 防腐等级
    "environmental_cert": "string"        // 环保认证
  },
  "inventory_quantity": "integer",        // 库存数量，≥0
  "inventory_status": "string",           // 库存状态: normal/shortage/presale
  "promotion_type": "string",             // 促销类型: discount/buy_gift/full_reduction
  "promotion_start_time": "datetime",     // 促销开始时间
  "promotion_end_time": "datetime",       // 促销结束时间
  "media_urls": ["string"],               // 产品图片/视频URL数组，至少1张图片
  "quality_report_url": "string",         // 质检报告URL，必填
  "production_standard": "string",        // 生产标准
  "unit_price": "decimal(2)",             // 单价
  "min_order_quantity": "integer",        // 最小起订量
  "supply_capacity": "integer",           // 供货能力
  "delivery_period": "integer"            // 供货周期（天）
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "供应信息发布成功",
  "data": {
    "product_id": "PROD-20240827-001",
    "status": "pending_review",           // 待审核
    "review_time": "2-24小时内完成审核",
    "detail_url": "/product/PROD-20240827-001"
  }
}
```

### 2.2 采购需求发布

**接口地址**: `POST /api/v1/info/demand`

**请求参数**:
```json
{
  "product_type": "string",               // 需求产品类型，必填
  "purchase_quantity": "integer",         // 采购数量，必填
  "quantity_unit": "string",              // 数量单位
  "quality_requirements": "string(100)",  // 质量要求，必填
  "delivery_period": "integer",           // 交货周期（天），必填
  "delivery_location": "string",          // 交货地点，必填
  "budget_amount": "decimal(2)",          // 预算金额，可选
  "demand_validity": "integer",           // 需求有效期（天），≥3
  "technical_specs": "text",              // 技术规格说明
  "attachment_urls": ["string"],          // 附件URL数组
  "contact_info": {                       // 联系信息
    "contact_person": "string(50)",
    "contact_phone": "string(11)",
    "contact_email": "string"
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "采购需求发布成功",
  "data": {
    "demand_id": "DEM-20240827-001",
    "status": "published",
    "matched_suppliers": 5,               // 匹配到的供应商数量
    "auto_push_time": "2024-08-27T10:35:00Z"
  }
}
```

### 2.3 招聘信息发布

**接口地址**: `POST /api/v1/info/recruitment`

**请求参数**:
```json
{
  "position_name": "string(30)",          // 岗位名称，必填
  "position_type": "string",              // 岗位类型: technical/construction/procurement/management
  "work_location": "string",              // 工作地点，必填
  "salary_range": "string",               // 薪资范围，必填
  "education_requirement": "string",      // 学历要求: college/bachelor/master
  "experience_requirement": "string",     // 工作经验: 1-3years/3-5years/5+years
  "position_requirements": "string(500)", // 岗位要求，必填
  "recruitment_deadline": "date",         // 招聘截止日期，必填
  "job_description": "text",              // 职位描述
  "benefits": "text",                     // 福利待遇
  "contact_info": {
    "contact_person": "string(50)",
    "contact_phone": "string(11)",
    "contact_email": "string"
  }
}
```

### 2.4 项目合作信息发布

**接口地址**: `POST /api/v1/info/cooperation`

**请求参数**:
```json
{
  "project_name": "string(50)",           // 项目名称，必填
  "project_type": "string",               // 项目类型: subcontract/equipment_sharing/technical_cooperation
  "project_period": "integer",            // 项目周期（天）
  "cooperation_budget": "decimal(2)",     // 合作预算
  "cooperation_requirements": "text",     // 合作要求，必填
  "project_location": "string",           // 项目地点
  "start_date": "date",                   // 预计开始日期
  "end_date": "date",                     // 预计结束日期
  "qualification_requirements": "text",   // 资质要求
  "contact_info": {
    "contact_person": "string(50)",
    "contact_phone": "string(11)",
    "contact_email": "string"
  }
}
```

### 2.5 技术问题发布

**接口地址**: `POST /api/v1/info/question`

**请求参数**:
```json
{
  "question_category": "string",          // 问题分类: material/construction/equipment/product_tech
  "question_title": "string(50)",        // 问题标题，必填
  "question_detail": "string(1000)",     // 问题详情，必填
  "attachment_urls": ["string"],          // 附件URL数组（图片/图纸）
  "urgency_level": "string",              // 紧急程度: low/medium/high
  "reward_points": "integer"              // 悬赏积分，可选
}
```

### 2.6 招投标信息发布

**接口地址**: `POST /api/v1/info/bidding`

**请求参数**:
```json
{
  "project_name": "string(50)",           // 项目名称，必填
  "bidding_type": "string",               // 招标类型: public/invitation
  "project_budget": "decimal(2)",         // 项目预算，必填
  "bidding_deadline": "datetime",         // 招标截止时间，必填
  "qualification_requirements": "string(500)", // 投标资质要求，必填
  "bidding_document_url": "string",       // 招标文件下载URL，必填
  "project_description": "text",          // 项目描述
  "project_location": "string",           // 项目地点
  "construction_period": "integer",       // 施工周期（天）
  "payment_terms": "text",                // 付款条件
  "contact_info": {
    "contact_person": "string(50)",
    "contact_phone": "string(11)",
    "contact_email": "string"
  }
}
```

## 3. 搜索与匹配系统模块

### 3.1 多维度搜索

**接口地址**: `GET /api/v1/search/multi-dimension`

**请求参数**:
```json
{
  "keyword": "string(50)",                // 关键词，可选
  "region": {                             // 地区筛选
    "province": "string",
    "city": "string",
    "district": "string"
  },
  "product_type": "string",               // 产品类型
  "supplier_rating": "string",            // 供应商评级: 1star/2star/3star/4star/5star
  "price_range": {                        // 价格区间
    "min_price": "decimal(2)",
    "max_price": "decimal(2)"
  },
  "delivery_period": "string",            // 供货周期: 1-3days/3-7days/7-15days/15+days
  "inventory_status": "string",           // 库存状态: normal/shortage/presale
  "search_type": "string",                // 搜索类型: supplier/product/demand/cooperation
  "sort_by": "string",                    // 排序方式: relevance/price_asc/price_desc/rating/delivery_time
  "page": "integer",                      // 页码，默认1
  "page_size": "integer"                  // 每页数量，默认10
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "搜索成功",
  "data": {
    "results": [
      {
        "id": "PROD-20240827-001",
        "type": "product",
        "name": "耐高温防腐涂料（150℃）",
        "supplier_name": "北京防腐材料有限公司",
        "supplier_rating": "4star",
        "price": 6500.00,
        "unit": "吨",
        "inventory_quantity": 500,
        "delivery_period": "3-7days",
        "location": "北京市朝阳区",
        "match_score": 95.5,               // 匹配度
        "thumbnail": "https://example.com/thumb.jpg"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total": 25,
      "total_pages": 3
    },
    "filters": {                          // 可用筛选项
      "available_regions": ["北京", "上海", "广东"],
      "available_types": ["防腐材料", "保温产品"],
      "price_range": {"min": 1000, "max": 50000}
    }
  }
}
```

### 3.2 智能推荐

**接口地址**: `GET /api/v1/search/recommendations`

**请求参数**:
```json
{
  "user_id": "string",                    // 用户ID
  "recommendation_type": "string",        // 推荐类型: supplier/demand/product
  "limit": "integer"                      // 推荐数量，默认5
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "推荐成功",
  "data": {
    "recommendations": [
      {
        "id": "SUP-202408-001",
        "type": "supplier",
        "name": "优质防腐材料供应商",
        "reason": "您近期搜索过防腐涂料",
        "score": 88.5,
        "thumbnail": "https://example.com/supplier.jpg",
        "key_info": {
          "rating": "4star",
          "main_products": ["防腐涂料", "保温材料"],
          "location": "北京市"
        }
      }
    ]
  }
}
```

### 3.3 供需自动匹配

**接口地址**: `POST /api/v1/search/auto-match`

**请求参数**:
```json
{
  "demand_id": "string",                  // 采购需求ID
  "match_criteria": {                     // 匹配条件
    "product_type_weight": "decimal",     // 产品类型权重，默认0.35
    "region_weight": "decimal",           // 地区权重，默认0.20
    "price_weight": "decimal",            // 价格权重，默认0.15
    "delivery_weight": "decimal",         // 供货周期权重，默认0.15
    "rating_weight": "decimal"            // 评级权重，默认0.15
  },
  "max_distance": "integer",              // 最大距离（公里），默认300
  "min_rating": "string"                  // 最低评级要求
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "匹配成功",
  "data": {
    "matched_suppliers": [
      {
        "supplier_id": "SUP-202408-001",
        "supplier_name": "北京防腐材料有限公司",
        "match_score": 92.5,
        "product_info": {
          "product_id": "PROD-20240827-001",
          "product_name": "耐高温防腐涂料",
          "price": 6500.00,
          "inventory": 500,
          "delivery_period": 5
        },
        "supplier_info": {
          "rating": "4star",
          "location": "北京市朝阳区",
          "distance": 25.5
        }
      }
    ],
    "total_matched": 8,
    "notification_sent": true              // 是否已发送通知
  }
}
```

### 3.4 关键词订阅管理

**接口地址**: `POST /api/v1/search/subscription`

**请求参数**:
```json
{
  "keywords": ["string"],                 // 订阅关键词数组
  "subscription_type": "string",          // 订阅类型: demand/supply/bidding
  "region": {                             // 地区限制，可选
    "province": "string",
    "city": "string"
  },
  "push_frequency": "string",             // 推送频率: realtime/daily
  "price_range": {                        // 价格范围，可选
    "min_price": "decimal(2)",
    "max_price": "decimal(2)"
  }
}
```

## 4. 沟通互动系统模块

### 4.1 发起会话

**接口地址**: `POST /api/v1/communication/conversation`

**请求参数**:
```json
{
  "target_user_id": "string",             // 目标用户ID
  "conversation_type": "string",          // 会话类型: inquiry/cooperation/technical_support
  "related_resource_id": "string",        // 关联资源ID（产品/需求/项目等）
  "initial_message": "string(500)"       // 初始消息
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "会话创建成功",
  "data": {
    "conversation_id": "CONV-20240827-001",
    "target_user_info": {
      "user_id": "USR-202408-002",
      "username": "supplier_user",
      "company_name": "北京防腐材料有限公司",
      "avatar": "https://example.com/avatar.jpg"
    },
    "created_at": "2024-08-27T10:30:00Z"
  }
}
```

### 4.2 发送消息

**接口地址**: `POST /api/v1/communication/message`

**请求参数**:
```json
{
  "conversation_id": "string",            // 会话ID
  "message_type": "string",               // 消息类型: text/file/image/quotation
  "content": "string(500)",               // 消息内容
  "file_url": "string",                   // 文件URL（文件消息时必填）
  "quotation_data": {                     // 报价数据（报价消息时必填）
    "product_id": "string",
    "quantity": "integer",
    "unit_price": "decimal(2)",
    "total_amount": "decimal(2)",
    "validity_period": "integer",         // 有效期（天）
    "payment_terms": "string",
    "delivery_period": "integer",
    "remarks": "string(300)"
  }
}
```

### 4.3 获取会话列表

**接口地址**: `GET /api/v1/communication/conversations`

**请求参数**:
```json
{
  "conversation_type": "string",          // 会话类型筛选，可选
  "status": "string",                     // 状态筛选: active/archived
  "page": "integer",
  "page_size": "integer"
}
```

### 4.4 获取消息历史

**接口地址**: `GET /api/v1/communication/messages/{conversation_id}`

**请求参数**:
```json
{
  "page": "integer",
  "page_size": "integer",
  "message_type": "string"                // 消息类型筛选，可选
}
```

### 4.5 报价议价

**接口地址**: `POST /api/v1/communication/negotiation`

**请求参数**:
```json
{
  "conversation_id": "string",            // 会话ID
  "original_quotation_id": "string",      // 原报价ID
  "new_price": "decimal(2)",              // 新报价
  "negotiation_reason": "string(200)",    // 议价理由，必填
  "counter_terms": {                      // 反提条件
    "payment_terms": "string",
    "delivery_period": "integer",
    "additional_services": "text"
  }
}
```

## 5. 资源整合中心模块

### 5.1 供应商资源管理

#### 5.1.1 供应商信息查询

**接口地址**: `GET /api/v1/resources/suppliers`

**请求参数**:
```json
{
  "supplier_id": "string",                // 供应商ID，可选
  "company_name": "string",               // 企业名称模糊查询
  "company_type": "string",               // 企业类型
  "rating": "string",                     // 评级筛选
  "region": {
    "province": "string",
    "city": "string"
  },
  "main_products": ["string"],            // 主营产品
  "certification_status": "string",       // 认证状态: verified/pending/rejected
  "page": "integer",
  "page_size": "integer"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "suppliers": [
      {
        "supplier_id": "SUP-202408-001",
        "company_name": "北京防腐材料有限公司",
        "company_type": "manufacturer",
        "rating": "4star",
        "location": "北京市朝阳区",
        "main_products": ["防腐涂料", "保温材料"],
        "established_year": 2010,
        "registered_capital": "5000万元",
        "certification_status": "verified",
        "certifications": [
          {
            "cert_type": "营业执照",
            "cert_number": "91110000123456789X",
            "valid_until": "2025-12-31"
          }
        ],
        "contact_info": {
          "contact_person": "张经理",
          "phone": "13800138000",
          "email": "zhang@example.com"
        },
        "business_scope": "防腐材料生产销售",
        "annual_output": "10000吨",
        "quality_certifications": ["ISO9001", "ISO14001"]
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total": 50,
      "total_pages": 5
    }
  }
}
```

#### 5.1.2 供应商产品管理

**接口地址**: `GET /api/v1/resources/supplier-products/{supplier_id}`

**请求参数**:
```json
{
  "product_type": "string",               // 产品类型筛选
  "inventory_status": "string",           // 库存状态筛选
  "price_range": {
    "min_price": "decimal(2)",
    "max_price": "decimal(2)"
  },
  "page": "integer",
  "page_size": "integer"
}
```

### 5.2 项目资源管理

#### 5.2.1 项目信息查询

**接口地址**: `GET /api/v1/resources/projects`

**请求参数**:
```json
{
  "project_type": "string",               // 项目类型: anticorrosion/insulation
  "project_status": "string",             // 项目状态: planning/bidding/construction/completed
  "region": {
    "province": "string",
    "city": "string"
  },
  "budget_range": {
    "min_budget": "decimal(2)",
    "max_budget": "decimal(2)"
  },
  "owner_company": "string",              // 甲方企业名称
  "page": "integer",
  "page_size": "integer"
}
```

### 5.3 人才资源管理

#### 5.3.1 人才信息查询

**接口地址**: `GET /api/v1/resources/talents`

**请求参数**:
```json
{
  "skill_type": "string",                 // 技能类型: anticorrosion/insulation/equipment
  "experience_years": "integer",          // 工作经验年限
  "education": "string",                  // 学历要求
  "location": {
    "province": "string",
    "city": "string"
  },
  "certification": ["string"],            // 持有证书
  "availability": "string",               // 可工作状态: available/busy
  "page": "integer",
  "page_size": "integer"
}
```

### 5.4 资料管理库

#### 5.4.1 技术资料查询

**接口地址**: `GET /api/v1/resources/technical-documents`

**请求参数**:
```json
{
  "document_type": "string",              // 文档类型: standard/regulation/process/case
  "category": "string",                   // 分类: material/construction/equipment
  "keyword": "string",                    // 关键词搜索
  "publish_date_range": {                 // 发布时间范围
    "start_date": "date",
    "end_date": "date"
  },
  "access_level": "string",               // 访问级别: public/member/vip
  "page": "integer",
  "page_size": "integer"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "documents": [
      {
        "document_id": "DOC-20240827-001",
        "title": "防腐涂料施工工艺标准",
        "document_type": "standard",
        "category": "construction",
        "publisher": "中国防腐保温技术协会",
        "publish_date": "2024-06-15",
        "file_size": "2.5MB",
        "download_url": "https://example.com/doc.pdf",
        "access_level": "member",
        "download_count": 1250,
        "description": "详细介绍防腐涂料的施工工艺流程和质量控制要点"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total": 120,
      "total_pages": 12
    }
  }
}
```

## 6. 商务服务平台模块

### 6.1 交易服务系统

#### 6.1.1 订单创建

**接口地址**: `POST /api/v1/business/orders`

**请求参数**:
```json
{
  "supplier_id": "string",                // 供应商ID，必填
  "buyer_id": "string",                   // 采购方ID，必填
  "order_items": [                        // 订单项目
    {
      "product_id": "string",
      "product_name": "string",
      "quantity": "integer",
      "unit_price": "decimal(2)",
      "total_price": "decimal(2)",
      "technical_requirements": "text"
    }
  ],
  "delivery_info": {                      // 交货信息
    "delivery_address": "string",
    "delivery_contact": "string",
    "delivery_phone": "string",
    "expected_delivery_date": "date"
  },
  "payment_terms": "string",              // 付款条件
  "special_requirements": "text",         // 特殊要求
  "contract_attachment": "string"         // 合同附件URL
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "订单创建成功",
  "data": {
    "order_id": "ORD-20240827-001",
    "order_number": "TX20240827001",
    "total_amount": 65000.00,
    "order_status": "pending_confirm",     // 待确认
    "created_at": "2024-08-27T10:30:00Z",
    "estimated_delivery": "2024-09-05"
  }
}
```

#### 6.1.2 订单状态更新

**接口地址**: `PUT /api/v1/business/orders/{order_id}/status`

**请求参数**:
```json
{
  "status": "string",                     // 订单状态: confirmed/production/shipped/delivered/completed
  "status_note": "string",                // 状态说明
  "tracking_number": "string",            // 物流单号（发货时必填）
  "estimated_delivery": "date",           // 预计交货日期
  "actual_delivery": "date",              // 实际交货日期
  "attachments": ["string"]               // 相关附件（如发货单、验收单）
}
```

### 6.2 库存管理工具

#### 6.2.1 库存更新

**接口地址**: `PUT /api/v1/business/inventory`

**请求参数**:
```json
{
  "updates": [                           // 批量更新
    {
      "product_id": "string",
      "quantity": "integer",              // 库存数量
      "operation_type": "string",         // 操作类型: set/add/subtract
      "warehouse_location": "string",     // 仓库位置
      "batch_number": "string",           // 批次号
      "expiry_date": "date",              // 有效期
      "cost_price": "decimal(2)",         // 成本价
      "note": "string"                    // 备注
    }
  ]
}
```

#### 6.2.2 库存预警设置

**接口地址**: `POST /api/v1/business/inventory/alerts`

**请求参数**:
```json
{
  "product_id": "string",                 // 产品ID
  "low_stock_threshold": "integer",       // 缺货预警阈值
  "overstock_threshold": "integer",       // 积压预警阈值
  "alert_methods": ["string"],            // 预警方式: sms/email/system_notification
  "alert_recipients": ["string"]          // 预警接收人用户ID数组
}
```

### 6.3 工程成本管理工具

#### 6.3.1 材料预算计算

**接口地址**: `POST /api/v1/business/cost/material-budget`

**请求参数**:
```json
{
  "project_id": "string",                 // 项目ID
  "project_area": "decimal(2)",           // 项目面积
  "construction_period": "integer",       // 施工工期（天）
  "material_requirements": [              // 材料需求
    {
      "material_type": "string",
      "specification": "string",
      "estimated_quantity": "decimal(2)",
      "unit": "string"
    }
  ],
  "price_fluctuation_factor": "decimal(2)" // 价格波动系数，默认1.0
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "预算计算成功",
  "data": {
    "budget_id": "BUD-20240827-001",
    "total_budget": 850000.00,
    "material_breakdown": [
      {
        "material_type": "防腐涂料",
        "quantity": 100,
        "unit": "吨",
        "unit_price": 6500.00,
        "subtotal": 650000.00,
        "supplier_options": [
          {
            "supplier_id": "SUP-202408-001",
            "supplier_name": "北京防腐材料有限公司",
            "quoted_price": 6500.00,
            "delivery_period": 7
          }
        ]
      }
    ],
    "price_analysis": {
      "base_cost": 800000.00,
      "fluctuation_impact": 50000.00,
      "risk_reserve": 5.88                // 风险储备百分比
    }
  }
}
```

## 7. 智能技术服务平台模块

### 7.1 AI技术问答系统

#### 7.1.1 提交技术问题

**接口地址**: `POST /api/v1/tech-service/questions`

**请求参数**:
```json
{
  "question_category": "string",          // 问题分类: material/construction/equipment/product_tech
  "question_title": "string(50)",        // 问题标题，必填
  "question_content": "string(1000)",    // 问题内容，必填
  "attachment_urls": ["string"],          // 附件URL数组
  "urgency_level": "string",              // 紧急程度: low/medium/high
  "related_product_id": "string",         // 关联产品ID，可选
  "project_context": "text"              // 项目背景，可选
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "问题提交成功",
  "data": {
    "question_id": "QST-20240827-001",
    "ai_preliminary_answer": {
      "confidence": 0.85,
      "answer_content": "根据您描述的低温环境防腐涂料开裂问题，建议采用以下解决方案...",
      "related_cases": [
        {
          "case_id": "CASE-001",
          "case_title": "东北地区低温防腐施工案例",
          "similarity": 0.92
        }
      ]
    },
    "expert_notification_sent": true,     // 是否已通知专家
    "estimated_response_time": "12小时内"
  }
}
```

#### 7.1.2 获取问题解答

**接口地址**: `GET /api/v1/tech-service/questions/{question_id}/answers`

**响应示例**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "question_info": {
      "question_id": "QST-20240827-001",
      "title": "低温环境下防腐涂料施工易开裂如何解决？",
      "content": "项目地点在东北，冬季温度-15℃...",
      "category": "construction",
      "created_at": "2024-08-27T09:00:00Z"
    },
    "answers": [
      {
        "answer_id": "ANS-20240827-001",
        "answerer_type": "expert",         // 回答者类型: ai/expert/supplier
        "answerer_info": {
          "user_id": "EXP-001",
          "name": "李工程师",
          "title": "高级防腐工程师",
          "rating": "5star"
        },
        "answer_content": "针对低温环境防腐涂料开裂问题，建议采用以下措施...",
        "attachments": [
          {
            "file_name": "低温施工指导书.pdf",
            "file_url": "https://example.com/guide.pdf"
          }
        ],
        "is_best_answer": true,            // 是否为最佳答案
        "likes": 15,                       // 点赞数
        "created_at": "2024-08-27T11:30:00Z"
      }
    ]
  }
}
```

### 7.2 专家咨询系统

#### 7.2.1 专家列表查询

**接口地址**: `GET /api/v1/tech-service/experts`

**请求参数**:
```json
{
  "expertise_field": "string",           // 专业领域: material/construction/equipment
  "rating": "string",                     // 专家评级筛选
  "consultation_price_range": {           // 咨询价格范围
    "min_price": "decimal(2)",
    "max_price": "decimal(2)"
  },
  "availability": "string",               // 可用状态: available/busy
  "consultation_method": "string",        // 咨询方式: online/offline/both
  "page": "integer",
  "page_size": "integer"
}
```

#### 7.2.2 预约专家咨询

**接口地址**: `POST /api/v1/tech-service/expert-consultation`

**请求参数**:
```json
{
  "expert_id": "string",                  // 专家ID，必填
  "consultation_type": "string",          // 咨询类型: process_guidance/problem_diagnosis
  "consultation_method": "string",        // 咨询方式: online/offline
  "problem_description": "text",         // 问题描述，必填
  "expected_duration": "integer",         // 预期时长（分钟）
  "preferred_time": "datetime",           // 期望时间
  "consultation_fee": "decimal(2)",       // 咨询费用
  "attachments": ["string"]               // 相关附件
}
```

## 8. 智能招投标平台模块

### 8.1 招投标资源库

#### 8.1.1 招标信息查询

**接口地址**: `GET /api/v1/bidding/tenders`

**请求参数**:
```json
{
  "project_type": "string",               // 项目类型
  "bidding_type": "string",               // 招标类型: public/invitation
  "region": {
    "province": "string",
    "city": "string"
  },
  "budget_range": {
    "min_budget": "decimal(2)",
    "max_budget": "decimal(2)"
  },
  "deadline_range": {                     // 截止时间范围
    "start_date": "date",
    "end_date": "date"
  },
  "status": "string",                     // 招标状态: open/closed/awarded
  "page": "integer",
  "page_size": "integer"
}
```

#### 8.1.2 投标文件生成

**接口地址**: `POST /api/v1/bidding/generate-proposal`

**请求参数**:
```json
{
  "tender_id": "string",                  // 招标ID，必填
  "company_info": {                       // 企业信息
    "company_id": "string",
    "qualification_docs": ["string"]      // 资质文件URL数组
  },
  "technical_proposal": {                 // 技术方案
    "construction_plan": "text",
    "quality_assurance": "text",
    "safety_measures": "text",
    "timeline": "text"
  },
  "commercial_proposal": {                // 商务方案
    "total_price": "decimal(2)",
    "payment_terms": "string",
    "warranty_period": "integer",
    "delivery_schedule": "text"
  },
  "supply_chain_plan": {                  // 供应链方案
    "supplier_partnerships": [
      {
        "supplier_id": "string",
        "product_type": "string",
        "supply_capacity": "integer"
      }
    ]
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "投标文件生成成功",
  "data": {
    "proposal_id": "PROP-20240827-001",
    "document_url": "https://example.com/proposal.pdf",
    "generation_time": "25分钟",
    "compliance_check": {
      "passed": true,
      "coverage_rate": 98.5,
      "missing_items": []
    },
    "file_size": "15.2MB"
  }
}
```

## 9. 数据中心模块

### 9.1 行业数据分析

#### 9.1.1 市场趋势分析

**接口地址**: `GET /api/v1/data/market-trends`

**请求参数**:
```json
{
  "analysis_type": "string",              // 分析类型: price/demand/supply/technology
  "product_category": "string",           // 产品类别
  "time_range": "string",                 // 时间范围: 1month/3months/6months/1year
  "region": "string",                     // 地区范围
  "comparison_dimension": "string"        // 对比维度: time/region/product
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "分析成功",
  "data": {
    "trend_analysis": {
      "overall_trend": "upward",          // 总体趋势: upward/downward/stable
      "growth_rate": 12.5,                // 增长率（%）
      "key_factors": [
        "原材料价格上涨",
        "环保政策推动",
        "基建投资增加"
      ]
    },
    "chart_data": {
      "labels": ["2024-01", "2024-02", "2024-03"],
      "datasets": [
        {
          "label": "防腐涂料价格",
          "data": [6200, 6350, 6500],
          "unit": "元/吨"
        }
      ]
    },
    "forecast": {
      "next_quarter_prediction": 6800,
      "confidence_level": 0.85
    }
  }
}
```

### 9.2 企业数据管理

#### 9.2.1 企业档案查询

**接口地址**: `GET /api/v1/data/enterprise-profiles`

**请求参数**:
```json
{
  "enterprise_id": "string",              // 企业ID
  "company_name": "string",               // 企业名称模糊查询
  "company_type": "string",               // 企业类型
  "region": "string",                     // 地区
  "registration_year_range": {            // 注册年份范围
    "start_year": "integer",
    "end_year": "integer"
  },
  "business_scope": "string",             // 经营范围关键词
  "page": "integer",
  "page_size": "integer"
}
```

## 10. 文件管理模块

### 10.1 文件上传

**接口地址**: `POST /api/v1/files/upload`

**请求参数**: `multipart/form-data`
```
file: File                              // 文件对象
file_type: string                       // 文件类型: image/document/video/certificate
category: string                        // 文件分类: product/qualification/technical/contract
description: string                     // 文件描述
```

**响应示例**:
```json
{
  "code": 200,
  "message": "文件上传成功",
  "data": {
    "file_id": "FILE-20240827-001",
    "file_name": "产品图片.jpg",
    "file_url": "https://cdn.example.com/files/2024/08/27/product.jpg",
    "file_size": 2048576,                 // 文件大小（字节）
    "file_type": "image",
    "mime_type": "image/jpeg",
    "upload_time": "2024-08-27T10:30:00Z",
    "cdn_url": "https://cdn.example.com/files/2024/08/27/product.jpg"
  }
}
```

### 10.2 文件下载

**接口地址**: `GET /api/v1/files/download/{file_id}`

**响应**: 文件流或重定向到CDN地址

## 11. 通知系统模块

### 11.1 发送通知

**接口地址**: `POST /api/v1/notifications/send`

**请求参数**:
```json
{
  "recipient_ids": ["string"],            // 接收者用户ID数组
  "notification_type": "string",          // 通知类型: system/business/marketing
  "title": "string(100)",                 // 通知标题
  "content": "text",                      // 通知内容
  "action_url": "string",                 // 操作链接，可选
  "send_methods": ["string"],             // 发送方式: system/sms/email/push
  "priority": "string",                   // 优先级: low/medium/high
  "scheduled_time": "datetime"            // 定时发送时间，可选
}
```

### 11.2 获取通知列表

**接口地址**: `GET /api/v1/notifications`

**请求参数**:
```json
{
  "status": "string",                     // 状态: unread/read/all
  "notification_type": "string",          // 通知类型筛选
  "date_range": {
    "start_date": "date",
    "end_date": "date"
  },
  "page": "integer",
  "page_size": "integer"
}
```

### 11.3 标记通知已读

**接口地址**: `PUT /api/v1/notifications/mark-read`

**请求参数**:
```json
{
  "notification_ids": ["string"]          // 通知ID数组
}
```

## 12. 系统配置模块

### 12.1 数据字典管理

#### 12.1.1 获取数据字典

**接口地址**: `GET /api/v1/config/dictionaries`

**请求参数**:
```json
{
  "dict_type": "string",                  // 字典类型: product_category/region/certification
  "parent_code": "string"                 // 父级编码，用于获取下级选项
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "dict_type": "product_category",
    "items": [
      {
        "code": "anticorrosion",
        "name": "防腐材料",
        "parent_code": null,
        "sort_order": 1,
        "children": [
          {
            "code": "coating",
            "name": "涂料",
            "parent_code": "anticorrosion",
            "sort_order": 1
          }
        ]
      }
    ]
  }
}
```

### 12.2 系统参数配置

#### 12.2.1 获取系统参数

**接口地址**: `GET /api/v1/config/system-params`

**响应示例**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "file_upload": {
      "max_file_size": 20971520,          // 最大文件大小（字节）
      "allowed_extensions": [".jpg", ".png", ".pdf", ".doc", ".docx"],
      "image_max_size": 5242880,          // 图片最大大小
      "video_max_size": 104857600         // 视频最大大小
    },
    "business_rules": {
      "auto_match_distance": 300,         // 自动匹配最大距离（公里）
      "quotation_validity_days": 7,       // 报价有效期（天）
      "max_negotiation_rounds": 5,        // 最大议价轮次
      "subscription_limits": {            // 订阅限制
        "normal_user": 5,
        "gold_member": 10,
        "diamond_member": 20
      }
    },
    "notification_settings": {
      "sms_daily_limit": 10,              // 短信日发送限制
      "email_batch_size": 100,            // 邮件批量发送大小
      "push_retry_times": 3               // 推送重试次数
    }
  }
}
```

## 13. 错误处理与异常情况

### 13.1 常见错误码

| 错误码 | 错误信息 | 说明 |
|--------|----------|------|
| 40001 | 参数缺失 | 必填参数未提供 |
| 40002 | 参数格式错误 | 参数类型或格式不正确 |
| 40003 | 参数值超出范围 | 参数值不在允许范围内 |
| 40101 | Token无效 | JWT Token过期或格式错误 |
| 40102 | 权限不足 | 用户无权限访问该资源 |
| 40301 | 资源不存在 | 请求的资源ID不存在 |
| 40302 | 资源已删除 | 资源已被删除或下架 |
| 42201 | 数据验证失败 | 业务规则验证不通过 |
| 42202 | 重复操作 | 重复提交相同请求 |
| 50001 | 服务器内部错误 | 系统异常 |
| 50002 | 数据库连接失败 | 数据库服务不可用 |
| 50003 | 第三方服务异常 | 外部服务调用失败 |

### 13.2 错误响应格式

```json
{
  "code": 40001,
  "message": "参数缺失",
  "error_detail": {
    "field": "product_name",
    "reason": "产品名称为必填字段"
  },
  "timestamp": "2024-08-27T10:30:00Z",
  "request_id": "req_123456789"
}
```