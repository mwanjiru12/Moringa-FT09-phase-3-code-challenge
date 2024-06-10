from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category
        if name is not None and category is not None:
            self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (new_name, self._id))
        conn.commit()
        conn.close()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        self._category = new_category
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (new_category, self._id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['author_id'], article['magazine_id']) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT authors.* FROM authors
        JOIN articles ON articles.author_id = authors.id
        WHERE articles.magazine_id = ?
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        titles = cursor.fetchall()
        conn.close()
        return [title['title'] for title in titles]

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT authors.*, COUNT(articles.id) as article_count FROM authors
        JOIN articles ON articles.author_id = authors.id
        WHERE articles.magazine_id = ?
        GROUP BY authors.id
        HAVING article_count > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]
