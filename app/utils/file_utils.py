import os
import zipfile

IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in IMAGE_EXTENSIONS


def is_3d_model(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    return ext in {"gltf", "glb", "obj", "fbx", "stl", "dae", "ply", "3ds"}


def get_file_size(file_path: str) -> tuple[int, str]:
    """Returns size_in_bytes"""
    if not file_path or not os.path.exists(file_path):
        return 0
    
    if file_path.lower().endswith(".zip"):
        return get_zip_file_size(file_path)
    
    return os.path.getsize(file_path)


def get_zip_file_size(zip_path: str) -> int:
    """Calculate total size of all files in a zip archive"""
    total_size = 0
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file_info in zip_ref.infolist():
                total_size += file_info.file_size
    except (zipfile.BadZipFile, OSError):
        return os.path.getsize(zip_path)
    return total_size


def get_file_size_from_upload(file_storage: str) -> int:
    """For file uploads - returns size in bytes"""
    file_storage.seek(0, os.SEEK_END)
    size_bytes = file_storage.tell()
    file_storage.seek(0)
    return size_bytes