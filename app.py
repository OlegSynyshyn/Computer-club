from flask import Flask, render_template, request, redirect, url_for
from db_scripts import DBManager
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime

IMG_PATH = os.path.dirname(__file__) + os.sep + 'static' + os.sep + 'Photos'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = DBManager("clubcom.db")

@app.route("/")
def index():
    categories = db.get_categories()
    articles = db.get_articles()
    return render_template("index.html", categories=categories, articles=articles)

@app.route("/category/<int:category_id>")
def category_page(category_id):
    categories = db.get_categories()
    articles = db.get_articles_by_category(category_id)
    return render_template("category.html", categories=categories, articles=articles, category_name=categories[category_id-1][1])

@app.route("/articles/<int:article_id>")
def article_page(article_id):
    categories = db.get_categories()
    article = db.get_article_by_id(article_id)
    return render_template("article.html", categories=categories, article=article)

@app.route("/articles/new", methods=["GET", "POST"])
def new_article():
    categories = db.get_categories()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['text']
        image = request.files['image']
        image.save(IMG_PATH + os.sep + image.filename)
        category_id = request.form['category']
        user_id = 1  # Припустимо, що користувач з ID 1 додає статтю
        db.create_article(user_id, category_id, title, content, image.filename)
        return redirect(url_for('index'))
    return render_template("new_article.html", categories=categories)

@app.route("/bookings/new", methods=["GET", "POST"])
def new_booking():
    if request.method == 'POST':
        user_id = 1  # Припустимо, що користувач з ID 1 робить запис
        start_time = request.form['start_time']
        db.create_booking(user_id, start_time)
        return redirect(url_for('index'))
    return render_template("new_booking.html")

@app.route("/search")
def search_page():
    categories = db.get_categories()
    query = request.args.get("query", '')
    articles = db.search_articles(query)
    return render_template("category.html", categories=categories, articles=articles, category_name=query)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)