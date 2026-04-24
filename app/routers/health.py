from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

router = APIRouter(tags=['health'])


@router.get('/health')
def health_check():
    return {
        'status': 'ok',
        'service': settings.APP_NAME,
        'version': settings.APP_VERSION,
    }


@router.get('/health/db')
def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
    except Exception as exc:
        raise HTTPException(status_code=503, detail='Database unavailable') from exc

    return {'status': 'ok', 'database': 'connected'}
