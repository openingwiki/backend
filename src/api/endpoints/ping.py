from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", description="Request for ping.")
async def ping():
    """
    Response with 200 status code.
    """
    return status.HTTP_200_OK