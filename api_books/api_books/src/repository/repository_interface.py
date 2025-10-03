from abc import ABC, abstractmethod


class IRepository(ABC):

    @abstractmethod
    def get_all_books(self):
        raise NotImplementedError

    @abstractmethod
    def get_book_by_id(self, book_id):
        raise NotImplementedError