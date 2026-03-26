from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core.database import Base
from app.main import app
from app.models.class_model import Class
from app.models.course import Course
from app.models.user import User

SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///:memory:'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _seed_class(db: Session) -> None:
    teacher = User(
        user_id=1,
        username='teacher1',
        password_hash='hashed',
        email='teacher1@example.com',
        real_name='Teacher One',
        role='teacher',
    )
    course = Course(
        course_id=1,
        course_name='Python 程序设计',
        course_code='CS102',
        semester='2025-2026-2',
        description='intro',
        teacher_id=1,
    )
    class_model = Class(
        class_id=1,
        course_id=1,
        class_name='A班',
        class_code='A-001',
        teacher_id=1,
    )
    db.merge(teacher)
    db.merge(course)
    db.merge(class_model)
    db.commit()


def test_assignment_crud_and_publish() -> None:
    db = TestingSessionLocal()
    _seed_class(db)
    db.close()

    create_resp = client.post(
        '/api/v1/assignments',
        json={
            'title': '作业一',
            'description': '基础题',
            'class_id': 1,
            'teacher_id': 1,
            'questions': ['q-1', 'q-2'],
            'due_date': '2026-04-01T12:00:00',
            'allow_resubmit': True,
        },
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created['title'] == '作业一'
    assert created['questions'] == ['q-1', 'q-2']
    assert created['is_published'] is False

    list_resp = client.get('/api/v1/assignments', params={'class_id': 1, 'teacher_id': 1})
    assert list_resp.status_code == 200
    listed = list_resp.json()
    assert len(listed) == 1
    assert listed[0]['assignment_id'] == created['assignment_id']

    aid = created['assignment_id']
    update_resp = client.put(
        f'/api/v1/assignments/{aid}',
        json={
            'title': '作业一-修订版',
            'questions': ['q-2', 'q-3'],
            'allow_resubmit': False,
        },
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated['title'] == '作业一-修订版'
    assert updated['questions'] == ['q-2', 'q-3']
    assert updated['allow_resubmit'] is False

    publish_resp = client.post(f'/api/v1/assignments/{aid}/publish')
    assert publish_resp.status_code == 200
    published = publish_resp.json()
    assert published['is_published'] is True
    assert published['published_at'] is not None

    published_list_resp = client.get('/api/v1/assignments', params={'is_published': True})
    assert published_list_resp.status_code == 200
    assert len(published_list_resp.json()) == 1


def test_update_and_publish_nonexistent_assignment() -> None:
    update_resp = client.put('/api/v1/assignments/999', json={'title': 'x'})
    assert update_resp.status_code == 404

    publish_resp = client.post('/api/v1/assignments/999/publish')
    assert publish_resp.status_code == 404
