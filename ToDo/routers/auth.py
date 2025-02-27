from fastapi import APIRouter

router = APIRouter()

@router.get('/get_user')
async def get_user():
    return "Hello World!"