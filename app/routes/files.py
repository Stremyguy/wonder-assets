import os
from flask import Blueprint, url_for, request, current_app
from werkzeug.utils import secure_filename
from app.services import allowed_file
from datetime import datetime

file_bp = Blueprint("files_bp", __name__)


@file_bp.route("/upload_image", methods=["POST"])
def upload_images() -> dict:
    if "upload" not in request.files:
        return {"error": {"message": "No file uploaded"}}, 400
    
    file = request.files["upload"]
    
    if file.filename == "":
        return {"error": {"message": "No selected file"}}, 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["IMAGES_FOLDER"], filename))
        
        return {
            "url": url_for("static", filename=f"images/items/{filename}", _external=True)
        }
    
    return {"error": {"message": "File type not allowed"}}, 400
