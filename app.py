from flask import Flask, session, redirect, url_for, flash , request , render_template , Response
from routes.pages import pages
from routes.api import api
from routes.viewer import viewer
import modules.dbmgmt as db
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(pages)
app.register_blueprint(api)
app.register_blueprint(viewer)



def render_sitemap(pages):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append("<url>")
        xml.append(f"<loc>{page['loc']}</loc>")
        xml.append(f"<lastmod>{page['lastmod']}</lastmod>")
        xml.append(f"<changefreq>{page['changefreq']}</changefreq>")
        xml.append(f"<priority>{page['priority']}</priority>")
        xml.append("</url>")

    xml.append("</urlset>")

    return "\n".join(xml)



@app.route("/sitemap.xml")
def sitemap():
    pages = []

    base_url = os.getenv("WEBSITE_BASE_URL")

    static_routes = [

        ]

    for route in static_routes:
        pages.append({
            "loc": base_url + url_for(route),
            "lastmod": datetime.utcnow().date().isoformat(),
            "changefreq": "weekly",
            "priority": "0.8"
        })

    blogs = db.blogs_meta.find(
        {"status": "published"},
        {"slug": 1, "updated_at": 1}
    )

    for blog in blogs:
        pages.append({
            "loc": f"{base_url}/blog/{blog['slug']}",
            "lastmod": blog.get("updated_at", datetime.utcnow()).date().isoformat(),
            "changefreq": "monthly",
            "priority": "0.9"
        })

    sitemap_xml = render_sitemap(pages)

    return Response(sitemap_xml, mimetype="application/xml")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # basic authentication for now

        user_name = os.getenv("BLOG_ADMIN_USERNAME")
        user_pwd = os.getenv("BLOG_ADMIN_PASSWORD")

        print(username , password , user_name , user_pwd)
        
        if username == user_name and password == user_pwd:
            session["user"] = {"username": username}
            return redirect(url_for("pages.dashboard"))
        else:
            flash("Invalid credentials", "error")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
