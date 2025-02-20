import sqlite3
from datetime import datetime

class DBManager():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = None

    def open_db(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
    
    def get_categories(self):
        self.open_db()
        self.cursor.execute('''SELECT * FROM categories''')
        data = self.cursor.fetchall()
        self.conn.close()
        return data
    
    def get_articles(self):
        self.open_db()
        self.cursor.execute('''SELECT * FROM articles''')
        data = self.cursor.fetchall()
        self.conn.close()
        return data

    def get_articles_by_category(self, category_id):
        self.open_db()
        self.cursor.execute('''SELECT * FROM articles WHERE category_id = ?''', [category_id])
        data = self.cursor.fetchall()
        self.conn.close()
        return data
    
    def get_article_by_id(self, article_id):
        self.open_db()
        self.cursor.execute('''SELECT * FROM articles WHERE id=?''', [article_id])
        data = self.cursor.fetchone()
        self.conn.close()
        return data
    
    def create_article(self, user_id, category_id, title, content, image):
        self.open_db()
        self.cursor.execute('''INSERT INTO articles (user_id, category_id, title, content, created_at) VALUES (?, ?, ?, ?, ?)''', 
                            [user_id, category_id, title, content, datetime.now()])
        self.conn.commit()
        self.conn.close()

    def create_booking(self, user_id, start_time):
        self.open_db()
        self.cursor.execute('''INSERT INTO bookings (user_id, start_time, status, created_at) VALUES (?, ?, ?, ?)''', 
                            [user_id, start_time, 'pending', datetime.now()])
        self.conn.commit()
        self.conn.close()

    def search_articles(self, query):
        self.open_db()
        query = '%' + query + '%'
        self.cursor.execute('''SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?''', [query, query])
        data = self.cursor.fetchall()
        self.conn.close()
        return data