from src.repository.repository_interface import IRepository


class BookRepository(IRepository):


    def get_all_books(self):
        pass

    def get_book_by_id(self, book_id):
        pass

    def __init__(self):
        self.books = {}