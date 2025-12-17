import uuid
from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime
import modules.dbmgmt as db
from utils import login_required

pages = Blueprint("pages", __name__)

@pages.route("/dashboard/")
@login_required
def dashboard():
    blogs = list(db.all_blogs())
    return render_template("dashboard.html", blogs=blogs)

@pages.route("/blog/create")
@login_required
def create_blog():
    blog_id = str(uuid.uuid4())
    now = datetime.utcnow()

    meta = {
        "blog_id": blog_id,
        "title": "Untitled Story",
        "slug": f"untitled-{blog_id[:8]}",
        "description": "",
        "thumbnail_url": "",
        "author": {"name": "AryCodes"},
        "status": "draft",
        "created_at": now,
        "updated_at": now
    }

    content = {
        "blog_id": blog_id,
        "content": "# New Blog Post\nStart writing here...",
        "updated_at": now
    }

    db.blogs_meta.insert_one(meta)
    db.blogs_content.insert_one(content)

    return redirect(url_for("pages.edit_blog", blog_id=blog_id))

@pages.route("/blog/edit/<blog_id>")
@login_required
def edit_blog(blog_id):
    meta = db.blogs_meta.find_one({"blog_id": blog_id}, {"_id": 0})
    content = db.blogs_content.find_one({"blog_id": blog_id}, {"_id": 0})

    if not meta:
        return "Blog not found", 404

    return render_template(
        "editor.html",
        blog_id=blog_id,
        meta=meta,
        content=content or {"content": ""}
    )
