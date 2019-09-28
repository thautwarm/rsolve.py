from .well_defined_forms import *
from functools import reduce


def normal(x: WFF[T]) -> NF[T]:
    if isinstance(x, Atom):
        return AtomN(x.a)
    if isinstance(x, And):
        return normal(x.l) & normal(x.r)
    if isinstance(x, Or):
        return normal(x.l) | normal((~x.l) & x.r)
    if isinstance(x, Imply):
        return normal((~x.cond) | x.then)
    if isinstance(x, Not):
        f = x.f
        if isinstance(f, Atom):
            k: AtomF[T] = f.a
            xs = k.not_a()
            if not xs:
                raise ValueError("Supplementary set of {} is empty".format(
                    repr(k)))
            return reduce(OrN, map(AtomN, xs))
        if isinstance(f, Not):
            return normal(f.f)
        if isinstance(f, And):
            return normal(~f.l) | normal(~f.r)

        if isinstance(f, Or):
            return normal(~f.l) & normal(~f.r)
        if isinstance(f, Imply):
            return normal(~f.cond | f.then)

    raise TypeError(type(x), x)
