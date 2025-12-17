from flask import Blueprint, request, jsonify , session
from datetime import datetime
import modules.dbmgmt as db
from utils import login_required


api = Blueprint("api", __name__, url_prefix="/api")

from utils import login_required

@api.before_request
def require_login_api():
    if "user" not in session:
        return {"error": "Unauthorized"}, 401

# Save Blog Content
@api.route("/blog/save-content/<blog_id>", methods=["POST"])
def save_content(blog_id):
    data = request.json or {}

    db.blogs_content.update_one(
        {"blog_id": blog_id},
        {"$set": {
            "content": data.get("content", ""),
            "updated_at": datetime.utcnow()
        }},
        upsert=True
    )
    return jsonify({"status": "saved"})

# Update Blog Metadata
@api.route("/blog/update-meta/<blog_id>", methods=["POST"])
def update_meta(blog_id):
    data = request.json or {}

    db.blogs_meta.update_one(
        {"blog_id": blog_id},
        {"$set": {
            "title": data.get("title"),
            "slug": data.get("slug"),
            "description": data.get("description"),
            "thumbnail_url": data.get("thumbnail"),
            "author": {"name": data.get("author")},
            "updated_at": datetime.utcnow()
        }}
    )
    return jsonify({"status": "meta_updated"})

# Toggle Publish Status
@api.route("/blog/status/<blog_id>", methods=["POST"])
def toggle_status(blog_id):
    data = request.json or {}
    new_status = data.get("status")

    if new_status not in ("published", "draft"):
        return jsonify({"error": "Invalid status"}), 400

    db.blogs_meta.update_one(
        {"blog_id": blog_id},
        {"$set": {
            "status": new_status,
            "published_at": datetime.utcnow() if new_status == "published" else None,
            "updated_at": datetime.utcnow()
        }}
    )
    return jsonify({"status": new_status})
