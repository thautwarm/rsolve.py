from dataclasses import dataclass

from rsolve.atom_formula import *

T = t.TypeVar('T', )


class WFF(t.Generic[T]):
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def then(self, other):
        return Imply(self, other)

    def __invert__(self):
        return Not(self)


@dataclass(frozen=True, order=True)
class Atom(WFF[T]):
    a: AtomF[T]


@dataclass(frozen=True, order=True)
class Not(WFF[T]):
    f: WFF[T]
    pass


@dataclass(frozen=True, order=True)
class And(WFF[T]):
    l: WFF[T]
    r: WFF[T]
    pass


@dataclass(frozen=True, order=True)
class Or(WFF[T]):
    l: WFF[T]
    r: WFF[T]
    pass


@dataclass(frozen=True, order=True)
class Imply(WFF[T]):
    cond: WFF[T]
    then: WFF[T]
    pass


class NF(t.Generic[T]):
    def __and__(self, other):
        return AndN(self, other)

    def __or__(self, other):
        return OrN(self, other)


@dataclass(frozen=True, order=True)
class AtomN(NF[T]):
    a: AtomF[T]
    pass


@dataclass(frozen=True, order=True)
class AndN(NF[T]):
    l: NF[T]
    r: NF[T]
    pass


@dataclass(frozen=True, order=True)
class OrN(NF[T]):
    l: NF[T]
    r: NF[T]
    pass
