import logging
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from .database import UPLOADS_DIR, UPLOADS_MOUNT_PATH

logger = logging.getLogger(__name__)


def save_upload_file(upload_file: UploadFile) -> str:
    """Save an uploaded file with a UUID filename and return its public URL path."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    extension = Path(upload_file.filename or "").suffix
    new_filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOADS_DIR / new_filename

    with file_path.open("wb") as file_obj:
        shutil.copyfileobj(upload_file.file, file_obj)

    return f"{UPLOADS_MOUNT_PATH}/{new_filename}"


def delete_upload_file(document_path: str | None) -> None:
    """Safely remove an uploaded document file from the uploads directory."""
    if not document_path:
        return

    filename = Path(document_path).name
    if not filename or filename in {".", ".."}:
        return

    uploads_root = UPLOADS_DIR.resolve()
    target = (uploads_root / filename).resolve()
    if target.parent != uploads_root:
        logger.warning("Refusing to delete file outside uploads dir: %s", document_path)
        return

    try:
        target.unlink(missing_ok=True)
    except OSError as exc:
        logger.error("Error deleting file %s: %s", target, exc)
