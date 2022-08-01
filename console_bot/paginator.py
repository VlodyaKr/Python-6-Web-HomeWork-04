from abc import ABC, abstractmethod

N = 3  # кількість записів для представлення


class AbstractPaginator(ABC):

    @abstractmethod
    def get_view(self):
        pass


class Paginator(AbstractPaginator):
    def __init__(self, data):
        self.data = data

    def get_view(self, func=None, sort_key=None):
        index, print_block = 1, '=' * 50 + '\n'
        is_empty = True
        data_values = self.data.values()
        if sort_key is not None:
            data_values = sorted(data_values, key=sort_key)
        for record in data_values:
            if func is None or func(record):
                is_empty = False
                print_block += str(record) + '\n' + '-' * 50 + '\n'
                if index < N:
                    index += 1
                else:
                    yield print_block
                    index, print_block = 1, '=' * 50 + '\n'
        if is_empty:
            yield None
        else:
            yield print_block
