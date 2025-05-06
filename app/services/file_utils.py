from flask import current_app

IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in IMAGE_EXTENSIONS


def is_3d_model(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    return ext in {"gltf", "glb", "obj", "fbx", "stl", "dae", "ply", "3ds"}
