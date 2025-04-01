import shutil

from fastapi import APIRouter, UploadFile
from src.tasks.tasks import resize_image

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post("/")
async def upload_image(file: UploadFile):
    file_path = image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(file_path)
