import os
import shutil
import uuid

from fastapi import UploadFile

UPLOADS_DIR = "/data/uploads"

# Ensure upload directory exists
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)


def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves an uploaded file with a unique name to prevent overwrites.
    Returns the relative path to be stored in the database.
    """
    # 1. Generate a unique ID
    unique_id = str(uuid.uuid4())
    print(f"Unique ID: {unique_id}")

    # 2. Get the original extension (e.g., .pdf, .jpg)
    # logic: split by dot, get the last part
    filename = upload_file.filename
    extension = os.path.splitext(filename)[1]  # returns ".pdf"
    print(f"Original extension: {extension}")

    # 3. Construct new filename: "a1b2-c3d4-e5f6.pdf"
    # Optional: You can keep the original name too: "uuid-policy.pdf"
    new_filename = f"{unique_id}{extension}"
    print(f"new filename: {new_filename}")

    file_path = os.path.join(UPLOADS_DIR, new_filename)
    print(f"file path: {file_path}")

    # 4. Save the content
    with open(file_path, "wb+") as file_obj:
        shutil.copyfileobj(upload_file.file, file_obj)

    return str(file_path)
