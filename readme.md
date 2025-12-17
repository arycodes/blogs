# Blog Management System

## A custom blog management system built using **Flask** and **MongoDB**.

This project is my attempt to build a simple blog management system from scratch. It allows an admin to create, edit, publish, and delete blog posts using a dashboard. The goal was to understand how blogs work behind the scenes using Flask and MongoDB, without relying on ready-made platforms.

## Requirements

* Python **3.10+**
* MongoDB (local or cloud)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/arycodes/blogs.git
cd blogs
```


### 2. Create virtual environment (Optional)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```


## Environment Variables

Create a `.env` file in the project root:

```env
MONGO_DB_URI=mongodburi
DB_NAME=dbname
BLOG_ADMIN_USERNAME=username
BLOG_ADMIN_PASSWORD=password
BLOG_PLATFORM_NAME=platformname
FLASK_SECRET_KEY=anysecretstring
WEBSITE_BASE_URL=yourwebsite.com
```


## Run the App

```bash
python app.py
```

Open:

```
http://localhost:5000
```


## Sitemap

```
/sitemap.xml
```


## Notes

* Admin routes require login
* Only published blogs appear publicly
* Dashboard and editor are protected

