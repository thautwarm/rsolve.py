from rsolve.normal import normal
from rsolve.well_defined_forms import Atom, Imply, Or
from rsolve.interface import MS
from rsolve.build_dnf import build_nf_
from dataclasses import dataclass
print('running test_wff.py')


@dataclass(frozen=True, order=True)
class P:
    v: str
    is_not: bool = True

    def not_a(self):
        return [P(self.v, not self.is_not)]

    def __repr__(self):
        if self.is_not:
            return f"not {self.v}"
        else:
            return self.v


p1 = Atom(P("p1"))
p2 = Atom(P("p2"))

x1 = normal(Or(p1, p2))

x2 = normal(Imply(p1, p2))

a1 = build_nf_(MS, x1)
a2 = build_nf_(MS, x2)

a = MS.combine(a1, a2)

for e in (a(set())):
    print(e)
