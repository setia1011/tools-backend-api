from fastapi import APIRouter
from app.v1.routers import home, cedict, ecdict, file

router = APIRouter()
router.include_router(home.router, prefix='', tags=['Home'])
router.include_router(file.router, prefix='/v1/api/file', tags=['file'])
router.include_router(cedict.router, prefix='/v1/api/cedict', tags=['cedict'])
router.include_router(ecdict.router, prefix='/v1/api/ecdict', tags=['ecdict'])