from flask import Flask, request
from flask.views import MethodView
from extension import db, cors
from models import Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors.init_app(app)


@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    Book.init_db()


@app.route('/')
def hello_world():
    return 'hello world!'


class BookApi(MethodView):
    def get(self, book_id):
        if not book_id:
            books: [Book] = Book.query.all()
            results = [
                {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_prize': book.book_prize,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author': book.author
                } for book in books
            ]
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        book: [Book] = Book.query.get(book_id)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results':
                {
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_prize': book.book_prize,
                    'book_number': book.book_number,
                    'book_publisher': book.book_publisher,
                    'author': book.author
                }
        }

    def post(self):
        form = request.json
        book = Book()
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.book_prize = form.get('book_prize')
        book.book_publisher = form.get('book_publisher')
        book.author = form.get('author')
        db.session.add(book)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据添加成功',
        }

    def delete(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功',
        }

    def put(self, book_id):
        book = Book.query.get(book_id)
        book.book_type = request.json.get('book_type')
        book.book_name = request.json.get('book_name')
        book.book_number = request.json.get('book_number')
        book.book_prize = request.json.get('book_prize')
        book.book_publisher = request.json.get('book_publisher')
        book.author = request.json.get('author')
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功',
        }


book_view = BookApi.as_view('book_api')
app.add_url_rule('/books/', defaults={'book_id': None},
                 view_func=book_view, methods=['GET', ])
app.add_url_rule('/books/',
                 view_func=book_view, methods=['POST'])
app.add_url_rule('/books/<int:book_id>', view_func=book_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
