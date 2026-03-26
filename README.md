# AutoGrader B-4 基础服务

B-4 是 AutoGrader 系统中的**基础服务模块**，负责提供统一的后端数据与认证能力。

## 已完成的基础骨架

当前仓库已经搭建好 FastAPI + SQLAlchemy 的基础项目结构，并预留了 `/api/v1` 下的核心业务路由：

- `auth`
- `users`
- `courses`
- `classes`
- `assignments`
- `grades`

同时已提供：

- 基础配置（`app/core/config.py`）
- 数据库连接与 Base（`app/core/database.py`）
- JWT 工具函数占位（`app/core/security.py`）
- 与需求文档一致的核心模型骨架（`users/students/teachers/courses/classes/assignments/submissions`）
- 一个基础健康检查测试（`tests/test_health.py`）

## 项目结构

```bash
.
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── assignments.py
│   │       ├── auth.py
│   │       ├── classes.py
│   │       ├── courses.py
│   │       ├── grades.py
│   │       └── users.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── assignment.py
│   │   ├── class_model.py
│   │   ├── course.py
│   │   ├── student.py
│   │   ├── submission.py
│   │   ├── teacher.py
│   │   └── user.py
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8004
```

访问：

- Health: `http://127.0.0.1:8004/health`
- OpenAPI: `http://127.0.0.1:8004/api/v1/openapi.json`

## 测试

```bash
pytest -q
```

## 下一步建议

1. 接入 Alembic 并生成第一版迁移。
2. 完成 RBAC（Student/Teacher/Admin）鉴权依赖。
3. 将占位路由替换为真实 CRUD + service 层。
4. 按文档完善导入学生（PDF/XLSX）与成绩导出（XLSX）。
