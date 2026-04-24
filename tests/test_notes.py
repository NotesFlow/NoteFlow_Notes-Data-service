import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = 'sqlite://'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_create_list_get_update_delete_note():
    create_response = client.post(
        '/internal/notes',
        json={
            'user_id': 1,
            'title': 'First note',
            'content': 'Hello NoteFlow',
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created['id'] == 1
    assert created['user_id'] == 1
    assert created['title'] == 'First note'

    list_response = client.get('/internal/notes?user_id=1')
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get('/internal/notes/1?user_id=1')
    assert get_response.status_code == 200
    assert get_response.json()['content'] == 'Hello NoteFlow'

    update_response = client.put(
        '/internal/notes/1',
        json={
            'user_id': 1,
            'title': 'Updated note',
            'content': 'Updated content',
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()['title'] == 'Updated note'

    delete_response = client.delete('/internal/notes/1?user_id=1')
    assert delete_response.status_code == 204

    missing_response = client.get('/internal/notes/1?user_id=1')
    assert missing_response.status_code == 404


def test_user_cannot_access_other_user_note():
    client.post(
        '/internal/notes',
        json={
            'user_id': 1,
            'title': 'Private note',
            'content': 'Secret',
        },
    )

    response = client.get('/internal/notes/1?user_id=2')
    assert response.status_code == 404
