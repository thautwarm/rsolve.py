from enum import Enum, auto as _auto
import abc
import typing as t
from dataclasses import dataclass


T = t.TypeVar('T', )


class HMT(t.Generic[T]):
    pass


@dataclass(frozen=True, order=True)
class TNom(HMT[T]):
    nom:T
    pass


@dataclass(frozen=True, order=True)
class TVar(HMT[T]):
    i:int
    pass


@dataclass(frozen=True, order=True)
class TFresh(HMT[T]):
    s:str
    pass


@dataclass(frozen=True, order=True)
class TArrow(HMT[T]):
    dom:HMT[T]
    codom:HMT[T]
    pass


@dataclass(frozen=True, order=True)
class TTup(HMT[T]):
    elts:t.Tuple[HMT[T],...]
    pass


@dataclass(frozen=True, order=True)
class TForall(HMT[T]):
    vars:t.FrozenSet[str]
    inst:HMT[T]
    pass


@dataclass(frozen=True, order=True)
class TApp(HMT[T]):
    fn:HMT[T]
    arg:HMT[T]
    pass
