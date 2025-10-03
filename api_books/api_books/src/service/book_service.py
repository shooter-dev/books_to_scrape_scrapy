class BookService:
    def __init__(self, book_repository):
        self.book_repository = book_repository

    def get_all_books(self):
        return self.book_repository.get_all()

    def get_book_by_id(self, book_id):
        return self.book_repository.get_by_id(book_id)

    def create_book(self, book_data):
        return self.book_repository.create(book_data)

    def update_book(self, book_id, book_data):
        return self.book_repository.update(book_id, book_data)

    def delete_book(self, book_id):
        return self.book_repository.delete(book_id)