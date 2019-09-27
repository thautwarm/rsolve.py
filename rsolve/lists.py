import typing as t


class Nil:
    nil = None
    __slots__ = []

    def __init__(self):
        if Nil.nil is None:
            Nil.nil = self
            return
        raise ValueError("Nil cannot get instantiated twice.")

    def __len__(self):
        return 0

    def __getitem__(self, n):
        raise IndexError('Out of bounds')

    @property
    def head(self):
        raise IndexError('Out of bounds')

    @property
    def tail(self):
        raise IndexError('Out of bounds')

    def __repr__(self):
        return "[]"


nil = Nil()

T = t.TypeVar("T")


class Cons(t.Generic[T]):
    head: T
    tail: 't.Union[Nil, Cons[T]]'

    def __init__(self, _head, _tail):
        self.head = _head
        self.tail = _tail

    def __len__(self):
        _nil = nil
        l = 0
        while self is not _nil:
            l += 1
            # noinspection PyMethodFirstArgAssignment
            self = self.tail
        return l

    def __iter__(self):
        _nil = nil
        while self is not _nil:
            yield self.head
            # noinspection PyMethodFirstArgAssignment
            self = self.tail

    def __getitem__(self, n):
        while n != 0:
            # noinspection PyMethodFirstArgAssignment
            self = self.tail
        return self.head

    def __repr__(self):
        return repr(list(self))
