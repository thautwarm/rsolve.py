import abc
from dataclasses import dataclass


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
    def seq(cls, ms):
        if not ms:

            return cls.pure(())

        def apply(ms_, ret=()):
            if not ms_:
                return cls.pure(ret)

            @cls.bind_curry(ms_[0])
            def k(a):
                return apply(ms_[1:], (a, *ret))

            return k

        return apply(ms)

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

    @staticmethod
    def gets(f):
        def get_(s):
            return (f(s), s),

        return get_

    @staticmethod
    def modify(f):
        def put_(s):
            return (None, f(s))

        return put_
