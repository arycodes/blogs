from flask import Blueprint, render_template , abort
import modules.dbmgmt as db
from dotenv import load_dotenv
import os

load_dotenv()


viewer = Blueprint("viewer", __name__)


BlogPlatformNamme = os.getenv("BLOG_PLATFORM_NAME")

@viewer.route("/")
def home():
    latest, blogs = db.published_blogs_with_latest_content()
    return render_template(
        "index.html",
        latest=latest,
        blogs=blogs,
        PlatformName = BlogPlatformNamme
    )


@viewer.route("/blog/<slug>")
def blog(slug):
    blog, blogs = db.get_blog_with_others(slug)

    if not blog:
        abort(404)

    return render_template(
        "blog.html",
        blog=blog,
        blogs=blogs,
        PlatformName = BlogPlatformNamme

    )


@viewer.route("/subscribe/")
def subscribe():
    return render_template(
        "newslettersignup.html",
        PlatformName = BlogPlatformNamme

    )