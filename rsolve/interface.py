import abc
from dataclasses import dataclass
import typing as t


class Monad(abc.ABC):
    @classmethod
    def combine(cls, a, b):
        def just_do(_):
            return b

        return cls.bind(a, just_do)

    @classmethod
    def bind_curry(cls, m):
        def then(k):
            return cls.bind(m, k)

        return then

    @classmethod
    @abc.abstractmethod
    def bind(cls, m, k):
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def pure(self, a):
        raise NotImplemented


@dataclass
class MS(Monad):
    @staticmethod
    def empty():
        return lambda s: ()

    @staticmethod
    def mplus(a, b):
        def plus(s):
            return a(s) + b(s)

        return plus

    @classmethod
    def bind(cls, m, k):
        def f(s):
            xs = m(s)

            def join():
                for (a, s_) in xs:

                    yield from k(a)(s_)

            return tuple(join())

        return f

    @classmethod
    def pure(cls, a):
        def ident(s):
            return (a, s),

        return ident

    @staticmethod
    def get(s):
        return (s, s),

    @staticmethod
    def put(s):
        return lambda _: ((None, s), )
