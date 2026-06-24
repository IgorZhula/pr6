from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Подключение к базе данных
engine = create_engine('sqlite:///library.db', echo=True)
print(engine)

Base = declarative_base()


# Описание моделей
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer)

    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', birth_year={self.birth_year})>"


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='books')

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', year={self.year}, author_id={self.author_id})>"


# Создание таблиц
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# 1. Добавление 3 авторов и 5 книг
author1 = Author(name='Лев Толстой', birth_year=1828)
author2 = Author(name='Фёдор Достоевский', birth_year=1821)
author3 = Author(name='Антон Чехов', birth_year=1860)

session.add_all([author1, author2, author3])
session.commit()

book1 = Book(title='Война и мир', year=1869, author=author1)
book2 = Book(title='Анна Каренина', year=1877, author=author1)
book3 = Book(title='Преступление и наказание', year=1866, author=author2)
book4 = Book(title='Идиот', year=1868, author=author2)
book5 = Book(title='Вишнёвый сад', year=1904, author=author3)

session.add_all([book1, book2, book3, book4, book5])
session.commit()

# 2. Вывод имен всех авторов
print("\n--- Все авторы ---")
authors = session.query(Author).all()
for author in authors:
    print(author.name)

# 3. Изменение имени одного автора
author_to_update = session.query(Author).filter_by(name='Лев Толстой').first()
if author_to_update:
    author_to_update.name = 'Лев Николаевич Толстой'
    session.commit()
    print(f"\nИмя автора изменено на: {author_to_update.name}")

# 4. Удаление одной книги
book_to_delete = session.query(Book).filter_by(title='Идиот').first()
if book_to_delete:
    session.delete(book_to_delete)
    session.commit()
    print(f"\nКнига '{book_to_delete.title}' удалена")

# 5. Все книги, отсортированные по году (от новых к старым)
print("\n--- Все книги (от новых к старым) ---")
books_by_year = session.query(Book).order_by(Book.year.desc()).all()
for book in books_by_year:
    print(f"{book.title} - {book.year}")

# 6. Книги, изданные после 1950 года
print("\n--- Книги после 1950 года ---")
books_after_1950 = session.query(Book).filter(Book.year > 1950).all()
if books_after_1950:
    for book in books_after_1950:
        print(f"{book.title} - {book.year}")
else:
    print("Книг после 1950 года не найдено")

# 7. Автор по конкретному имени
print("\n--- Поиск автора по имени 'Фёдор Достоевский' ---")
author_search = session.query(Author).filter_by(name='Фёдор Достоевский').first()
if author_search:
    print(f"Найден автор: {author_search.name} (род. {author_search.birth_year})")
    print(f"Его книги: {', '.join([book.title for book in author_search.books])}")
else:
    print("Автор не найден")

# 8. Количество книг через func.count()
book_count = session.query(func.count(Book.id)).scalar()
print(f"\n--- Общее количество книг в библиотеке: {book_count} ---")

# 9. Первые 3 книги в алфавитном порядке
print("\n--- Первые 3 книги в алфавитном порядке ---")
first_three_books = session.query(Book).order_by(Book.title).limit(3).all()
for book in first_three_books:
    print(f"{book.title} - {book.year}")

# Закрытие сессии
session.close()