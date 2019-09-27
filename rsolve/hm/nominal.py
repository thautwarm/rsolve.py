from enum import Enum, auto as _auto
import abc
import typing as t
from dataclasses import dataclass


class Type:
    pass


@dataclass(frozen=True, order=True)
class Int(Type):
    bit:int
    pass


@dataclass(frozen=True, order=True)
class Float(Type):
    bit:int
    pass


@dataclass(frozen=True, order=True)
class Text(Type):
    n:int
    pass


@dataclass(frozen=True, order=True)
class Bool(Type):
    pass


@dataclass(frozen=True, order=True)
class Any(Type):
    pass


@dataclass(frozen=True, order=True)
class Sig(Type):
    qual:str
    pass
