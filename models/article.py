from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author_id, magazine_id, title, id=None):
        self._id = id
        self._author_id = author_id
        self._magazine_id = magazine_id
        self._title = title
        if id is None:
            self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)',
                       (self._title, self._author_id, self._magazine_id))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self._author_id,))
        author = cursor.fetchone()
        conn.close()
        return Author(author['id'], author['name'])

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self._magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return Magazine(magazine['id'], magazine['name'], magazine['category'])
