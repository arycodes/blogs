from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv("MONGO_DB_URI"))
db = client[os.getenv("DB_NAME")]


blogs_meta = db.blogs_meta
blogs_content = db.blogs_content

blogs_meta.create_index("slug", unique=True)
blogs_content.create_index("blog_id", unique=True)


import uuid
from datetime import datetime


def create_blog(author_name: str):
    blog_id = f"b_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow()

    # META
    blogs_meta.insert_one({
        "blog_id": blog_id,
        "title": "Untitled Blog",
        "slug": f"draft-{blog_id}",
        "description": "",
        "thumbnail_url": "",
        "author": {"name": author_name},
        "topics": [],
        "status": "draft",
        "created_at": now,
        "updated_at": now
    })

    # CONTENT
    blogs_content.insert_one({
        "blog_id": blog_id,
        "content": "",
        "updated_at": now
    })

    return {
        "status": "ok",
        "blog_id": blog_id
    }



def save_blog_content(blog_id, content):
    blogs_content.update_one(
        {"blog_id": blog_id},
        {"$set": {
            "content": content,
            "updated_at": datetime.utcnow()
        }}
    )


def save_blog_meta(blog_id, data):
    data["updated_at"] = datetime.utcnow()

    blogs_meta.update_one(
        {"blog_id": blog_id},
        {"$set": data}
    )

def publish_blog(blog_id):
    blogs_meta.update_one(
        {"blog_id": blog_id},
        {"$set": {
            "status": "published",
            "updated_at": datetime.utcnow()
        }}
    )


def unpublish_blog(blog_id):
    blogs_meta.update_one(
        {"blog_id": blog_id},
        {"$set": {
            "status": "draft",
            "updated_at": datetime.utcnow()
        }}
    )


def all_blogs():
    return list(
        blogs_meta.find({}, {"_id": 0})
        .sort("created_at", -1)
    )


def get_blog_by_slug(slug):
    meta = blogs_meta.find_one(
        {"slug": slug, "status": "published"},
        {"_id": 0}
    )

    if not meta:
        return None

    content = blogs_content.find_one(
        {"blog_id": meta["blog_id"]},
        {"_id": 0}
    )

    return {
        "meta": meta,
        "content": content.get("content", "") if content else ""
    }


def published_blogs_with_latest_content():
    metas = list(
        blogs_meta.find(
            {"status": "published"},
            {"_id": 0}
        ).sort("created_at", -1)
    )

    if not metas:
        return None, []

    latest_meta = metas[0]

    content_doc = blogs_content.find_one(
        {"blog_id": latest_meta["blog_id"]},
        {"_id": 0}
    )

    latest = {
        "meta": latest_meta,
        "content": content_doc.get("content", "") if content_doc else ""
    }

    return latest, metas[1:]


def get_blog_with_others(slug):
    meta = blogs_meta.find_one(
        {"slug": slug, "status": "published"},
        {"_id": 0}
    )

    if not meta:
        return None, []

    content_doc = blogs_content.find_one(
        {"blog_id": meta["blog_id"]},
        {"_id": 0}
    )

    others = list(
        blogs_meta.find(
            {
                "status": "published",
                "slug": {"$ne": slug}
            },
            {"_id": 0}
        ).sort("created_at", -1)
    )

    blog = {
        "meta": meta,
        "content": content_doc.get("content", "") if content_doc else ""
    }

    return blog, others
