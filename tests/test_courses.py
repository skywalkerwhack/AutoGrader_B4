from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core.database import Base
from app.main import app
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


def _seed_teacher(db: Session) -> None:
    teacher = User(
        user_id=1,
        username='teacher1',
        password_hash='hashed',
        email='teacher1@example.com',
        real_name='Teacher One',
        role='teacher',
    )
    db.merge(teacher)
    db.commit()


def test_course_crud() -> None:
    db = TestingSessionLocal()
    _seed_teacher(db)
    db.close()

    create_resp = client.post(
        '/api/v1/courses',
        json={
            'course_name': 'Python 程序设计',
            'course_code': 'CS102',
            'semester': '2025-2026-2',
            'description': 'intro',
            'teacher_id': 1,
        },
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created['course_code'] == 'CS102'

    list_resp = client.get('/api/v1/courses', params={'teacher_id': 1, 'semester': '2025-2026-2'})
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    cid = created['course_id']
    get_resp = client.get(f'/api/v1/courses/{cid}')
    assert get_resp.status_code == 200

    update_resp = client.put(f'/api/v1/courses/{cid}', json={'description': 'updated'})
    assert update_resp.status_code == 200
    assert update_resp.json()['description'] == 'updated'

    delete_resp = client.delete(f'/api/v1/courses/{cid}')
    assert delete_resp.status_code == 204

    missing_resp = client.get(f'/api/v1/courses/{cid}')
    assert missing_resp.status_code == 404


def test_create_course_duplicate_code_semester_conflict() -> None:
    db = TestingSessionLocal()
    _seed_teacher(db)
    db.add(
        Course(
            course_name='Data Struct',
            course_code='CS200',
            semester='2025-2026-2',
            description=None,
            teacher_id=1,
        )
    )
    db.commit()
    db.close()

    resp = client.post(
        '/api/v1/courses',
        json={
            'course_name': 'Another Course',
            'course_code': 'CS200',
            'semester': '2025-2026-2',
            'description': None,
            'teacher_id': 1,
        },
    )

    assert resp.status_code == 409
