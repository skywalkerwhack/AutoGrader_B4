# AutoGrader B-4 基础服务

B-4 是 AutoGrader 系统中的**基础服务模块**，负责提供统一的后端数据与认证能力，主要包括：

- 用户认证与登录
- 用户信息管理
- 课程管理
- 班级管理
- 作业管理
- 成绩查询
- 为 B-1 前端、B-2 评测模块提供基础数据支持

---

## 1. 项目定位

在 AutoGrader 系统中，各模块职责大致如下：

- **B-1**：前端界面（学生端 / 教师端 / 管理员端）
- **B-2**：代码提交与评测调度
- **B-3**：题库管理与代码评测执行
- **B-4**：基础数据服务与认证中心

本项目即 **B-4 模块**，是系统的核心业务数据层，负责保存用户、课程、班级、作业、提交结果等关键数据。

---

## 2. 技术栈

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **Pydantic**
- **Uvicorn**
- **Alembic**（数据库迁移，推荐）
- **JWT**（身份认证）

---

## 3. 主要功能

### 3.1 认证模块
- 用户登录
- 用户登出
- Token 刷新
- 密码重置

### 3.2 用户模块
- 获取当前用户信息
- 修改个人信息
- 管理员查看用户列表
- 管理员创建教师账号
- 管理员停用账号

### 3.3 课程模块
- 教师创建课程
- 查询课程列表
- 获取课程详情
- 修改课程信息
- 删除课程

### 3.4 班级模块
- 教师创建班级
- 查询班级列表
- 查看班级学生列表
- 手动添加学生
- 移除学生
- 批量导入学生（后续）

### 3.5 作业模块
- 创建作业
- 查询作业列表
- 修改作业
- 发布作业

### 3.6 成绩模块
- 学生查询个人成绩
- 教师查询班级成绩
- 教师导出成绩单

---

## 4. 项目结构建议

可参考如下目录组织：

```bash
b4/
├── app/
│   ├── api/                  # 路由层
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── courses.py
│   │       ├── classes.py
│   │       ├── assignments.py
│   │       └── grades.py
│   ├── core/                 # 核心配置
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/               # SQLAlchemy 模型
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── teacher.py
│   │   ├── course.py
│   │   ├── class_model.py
│   │   ├── assignment.py
│   │   └── submission.py
│   ├── schemas/              # Pydantic 数据模型
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── class_schema.py
│   │   ├── assignment.py
│   │   └── grade.py
│   ├── services/             # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   ├── class_service.py
│   │   ├── assignment_service.py
│   │   └── grade_service.py
│   ├── utils/                # 工具函数
│   └── main.py               # FastAPI 入口
│
├── alembic/                  # 数据库迁移
├── tests/                    # 测试代码
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
