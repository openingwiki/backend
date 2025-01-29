from fastapi import APIRouter

router = APIRouter()


@router.get("/", description="Request for ping.")
async def ping():
    """
    Response with 200 status code.
    """
    return 200