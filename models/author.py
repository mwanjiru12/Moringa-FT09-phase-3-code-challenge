from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = name
        if name is not None:
            self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['author_id'], article['magazine_id']) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT magazines.* FROM magazines
        JOIN articles ON articles.magazine_id = magazines.id
        WHERE articles.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]
 