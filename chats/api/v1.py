from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_chats():
    return "chats app created!"
