import typing as t
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

T = t.TypeVar("T")


class AtomF(Protocol[T]):
    def not_a(self) -> t.List['AtomF[T]']:
        ...
