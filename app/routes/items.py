import os
from flask import Blueprint, render_template, redirect, flash, abort, request, url_for
from flask_login import login_required, current_user
from app.services import get_category_by_id, get_item_by_id, get_all_items, get_all_roles, filter_visible_items
from app.services import create_item as create_item_service
from app.services import edit_item as edit_item_service
from app.services import delete_item as delete_item_service
from app.services import is_3d_model
from app.permissions import has_permission, permission_required
from app.forms import ItemForm
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory

item_bp = Blueprint("items", __name__)


@item_bp.route("/items/<int:item_id>")
def item_page(item_id: int) -> str:
    item = get_item_by_id(item_id)
    
    @login_required
    def get_info_about_creator() -> bool:
        is_creator = item.creator_id == current_user.id
        can_edit_own = has_permission(current_user, "edit_own_item")
        can_edit_all = has_permission(current_user, "edit_item")
        can_delete_own = has_permission(current_user, "delete_own_item")
        can_delete_all = has_permission(current_user, "delete_item")
        
        return (is_creator and (can_edit_own and can_delete_own)) or (can_edit_all and can_delete_all)

    can_change_data = get_info_about_creator() if current_user.is_authenticated else False
    
    is_3d_item = False
    model_path = None
    
    if item.item_url:
        ext = item.item_url.rsplit(".", 1)[1].lower() if "." in item.item_url else ""
        if ext in {"gltf", "glb", "obj", "fbx", "stl", "dae", "ply", "3ds"}:
            is_3d_item = True
            model_path = url_for("static", filename=f"items/{item.item_url}")
        
    params = {
        "title": "Wonder assets",
        "item": item,
        "can_change_data": can_change_data,
        "is_3d_item": is_3d_item,
        "model_path": model_path
    }
    
    return render_template("item.html", **params)


@item_bp.route("/categories/<int:category_id>/items", methods=["GET", "POST"])
@login_required
def create_item(category_id: int) -> str:
    form = ItemForm()
    category = get_category_by_id(category_id)
    
    if not category:
        abort(404)
    
    params = {
        "title": "Wonder assets",
        "form": form,
    }

    if form.validate_on_submit():
        try:
            item_filename = None
            
            if form.item_url.data:
                item_file = form.item_url.data
                item_filename = secure_filename(item_file.filename)
                item_path = os.path.join(current_app.config["ITEMS_FOLDER"], item_filename)
                
                if os.path.exists(item_path):
                    flash("A file with this name already exists", "error")
                    return render_template("item_form.html", **params)

                os.makedirs(current_app.config["ITEMS_FOLDER"], exist_ok=True)
                item_file.save(item_path)

            image_filenames = []
            
            for image in form.images.data:
                if image:
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(current_app.config["IMAGES_FOLDER"], filename)
                    os.makedirs(current_app.config["IMAGES_FOLDER"], exist_ok=True)
                    image.save(image_path)
                    image_filenames.append(filename)

            description = request.form.get("description", "")
            
            create_item_service(
                title=form.title.data,
                description=description,
                item_url=item_filename,
                images=image_filenames if image_filenames else None,
                category_id=category_id,
                creator_id=current_user.id,
                type_id=form.type.data,
                show_meta=form.show_meta.data,
                is_private=form.is_private.data,
                can_download=form.can_download.data
            )
            
            return redirect(f"/categories/{category_id}")
        except Exception as exc:
            current_app.logger.error(f"Error creating item: {str(exc)}")
            flash("Error creating item. Please try again.", "error")
    return render_template("item_form.html", **params)


@item_bp.route("/items/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id: int) -> str:
    item = get_item_by_id(item_id)
    if not item:
        abort(404)
    
    is_creator = item.creator_id == current_user.id
    can_edit_own = has_permission(current_user, "edit_own_item")
    can_edit_all = has_permission(current_user, "edit_item")
    
    if not (is_creator and can_edit_own) and not can_edit_all:
        abort(403)
    
    form = ItemForm()
    current_images = [img for img in item.images if img.image_url != "item_logo_default.png"]
    
    if request.method == "GET":
        form.title.data = item.title
        form.description.data = item.description
        form.type.data = item.type_id
        form.is_private.data = item.is_private
        form.show_meta.data = item.show_meta
        form.can_download.data = item.can_download
    
    if form.validate_on_submit():
        try:
            item_filename = item.item_url
            
            if form.item_url.data:
                new_file = form.item_url.data
                new_filename = secure_filename(new_file.filename)
                new_path = os.path.join(current_app.config["ITEMS_FOLDER"], new_filename)
                
                if new_filename != item.item_url and os.path.exists(new_path):
                    flash("A file with this name already exists", "error")
                    return render_template("item_form.html",
                                         title="Wonder assets",
                                         form=form,
                                         item=item,
                                         current_images=current_images,
                                         is_edit=True)

                os.makedirs(current_app.config["ITEMS_FOLDER"], exist_ok=True)
                new_file.save(new_path)
                
                if item.item_url and item.item_url != "item_logo_default.png" and item.item_url != new_filename:
                    old_path = os.path.join(current_app.config["ITEMS_FOLDER"], item.item_url)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                item_filename = new_filename
            
            image_filenames = request.form.getlist("existing_images")
            
            if form.images.data:
                for image in form.images.data:
                    if image.filename:
                        filename = secure_filename(image.filename)
                        base, ext = os.path.splitext(filename)
                        counter = 1
                        
                        while os.path.exists(os.path.join(current_app.config["IMAGES_FOLDER"], filename)):
                            filename = f"{base}_{counter}{ext}"
                            counter += 1
                        
                        image_path = os.path.join(current_app.config["IMAGES_FOLDER"], filename)
                        os.makedirs(current_app.config["IMAGES_FOLDER"], exist_ok=True)
                        image.save(image_path)
                        image_filenames.append(filename)
            
            if not image_filenames:
                image_filenames = ["item_logo_default.png"]

            description = request.form.get("description", "")
            
            edit_item_service(
                item_id=item_id,
                title=form.title.data,
                description=description,
                item_url=item_filename,
                images=image_filenames,
                category_id=item.category_id,
                creator_id=item.creator_id,
                type_id=form.type.data,
                show_meta=form.show_meta.data,
                is_private=form.is_private.data,
                can_download=form.can_download.data
            )
            
            flash("Item updated successfully!", "success")
            return redirect(url_for("items.item_page", item_id=item_id))
            
        except Exception as exc:
            current_app.logger.error(f"Error editing item: {str(exc)}")
            flash("Error editing item. Please try again.", "error")
    
    return render_template("item_form.html",
                         title="Wonder assets",
                         form=form,
                         item=item,
                         current_images=current_images,
                         is_edit=True)


@item_bp.route("/items/delete/<int:item_id>", methods=["GET", "POST"])
@login_required
def delete_item(item_id: int) -> str:
    item = get_item_by_id(item_id)
    category_id = item.category_id
    
    if not item:
        abort(404)
    
    is_creator = item.creator_id == current_user.id
    can_delete_own = has_permission(current_user, "delete_own_item")
    can_delete_all = has_permission(current_user, "delete_item")
    
    if not (is_creator and can_delete_own) and not can_delete_all:
        abort(403)
    
    delete_item_service(item_id)
    return redirect(f"/categories/{category_id}")


@item_bp.route("/download/<filename>")
def download_file(filename: str) -> None:
    if ".." in filename or filename.startswith("/"):
        abort(403)
    
    file_path = os.path.join(current_app.config["ITEMS_FOLDER"], filename)
    
    if not os.path.exists(file_path):
        abort(404)
    
    return send_from_directory(
        directory=current_app.config["ITEMS_FOLDER"],
        path=filename,
        as_attachment=True
    )


@item_bp.route("/upload")
def upload_images() -> str:
    return "OK"
