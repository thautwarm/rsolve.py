from .well_defined_forms import *
from .interface import MS
import typing as t


def build_nf_(self: t.Type[MS], x: NF[T]):

    if isinstance(x, AtomN):
        a = x.a

        @self.bind_curry(self.get)
        def flow(s: set):
            return self.put({*s, a})

        return flow

    if isinstance(x, AndN):
        m1 = build_nf_(self, x.l)
        m2 = build_nf_(self, x.r)
        return self.combine(m1, m2)

    if isinstance(x, OrN):
        m1 = build_nf_(self, x.l)
        m2 = build_nf_(self, x.r)
        return self.mplus(m1, m2)

    raise TypeError(x)
