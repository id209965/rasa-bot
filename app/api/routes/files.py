from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid
import aiofiles
from pathlib import Path
from PIL import Image

from app.config import settings
from app.database.connection import get_session

router = APIRouter()

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_SIZE = (1024, 1024)  # Max dimensions for images


async def validate_and_resize_image(file_path: str) -> bool:
    """Validate and resize image if needed"""
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize if too large
            if img.size[0] > MAX_IMAGE_SIZE[0] or img.size[1] > MAX_IMAGE_SIZE[1]:
                img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
                img.save(file_path, "JPEG", quality=85, optimize=True)
            
            return True
    except Exception as e:
        print(f"Image validation failed: {e}")
        return False


@router.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    """Upload and store user/event photo"""
    
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")
    
    # Check file size
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="Файл слишком большой")
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.photos_dir, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)
    
    # Validate and resize image
    if not await validate_and_resize_image(file_path):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Неверный формат изображения")
    
    return {
        "filename": unique_filename,
        "url": f"/static/photos/{unique_filename}",
        "message": "Фотография успешно загружена"
    }


@router.get("/photo/{filename}")
async def get_photo(filename: str):
    """Get uploaded photo"""
    file_path = os.path.join(settings.photos_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Фотография не найдена")
    
    return FileResponse(file_path)


@router.delete("/photo/{filename}")
async def delete_photo(
    filename: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete uploaded photo"""
    file_path = os.path.join(settings.photos_dir, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Фотография удалена"}
    
    raise HTTPException(status_code=404, detail="Фотография не найдена")
