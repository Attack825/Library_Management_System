from extension import db


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_number = db.Column(db.String(255), nullable=False)
    book_name = db.Column(db.String(255), nullable=False)
    book_type = db.Column(db.String(255), nullable=False)
    book_prize = db.Column(db.Float, nullable=False)
    author = db.Column(db.String(255))
    book_publisher = db.Column(db.String(255))

    @staticmethod
    def init_db():
        rets = [
            (1, '001', '活着', '小说', 39.9, '余华', '某某出版社'),
            (2, '002', '三体', '科幻', 39.4, '刘慈欣', '重庆出版社')
        ]
        for ret in rets:
            book = Book()
            book.id = ret[0]
            book.book_number = ret[1]
            book.book_name = ret[2]
            book.book_type = ret[3]
            book.book_prize = ret[4]
            book.author = ret[5]
            book.book_publisher = ret[6]
            db.session.add(book)
        db.session.commit()
