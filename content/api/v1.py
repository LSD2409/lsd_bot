from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_content():
    return "content app created!"
