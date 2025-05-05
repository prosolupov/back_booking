from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post("/")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Ручка для загрузки картинок
    """
    ImagesService().upload_image(file, background_tasks)
    return {"status": "success"}
