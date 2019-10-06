from rsolve.hm import hm
from dataclasses import dataclass, field
import typing as t
Ext = t.TypeVar("Ext")


@dataclass
class TCEnv(t.Generic[Ext]):
    ext: Ext
    tvars: t.List[hm.HMT] = field(default_factory=list)
    neqs: t.Set[t.Tuple[hm.HMT, hm.HMT]] = field(default_factory=list)

    def new_tvar(self) -> hm.TVar:
        i = len(self.tvars)
        var = hm.TVar(i)
        self.tvars.append(var)
        return var

    def load_tvar(self, i: int) -> hm.HMT:
        return self.tvars[i]

    def occur_in(self, i: int, hmt: hm.HMT) -> bool:
        def contains(x: hm.HMT):
            if isinstance(x, hm.TApp):
                a = contains(x.fn)
                b = contains(x.arg)
                return a or b

            elif isinstance(x, hm.TArrow):
                a = contains(x.dom)
                b = contains(x.codom)
                return a or b
            elif isinstance(x, hm.TTup):
                elts = map(contains, x.elts)
                return any(elts)
            elif isinstance(x, hm.TForall):
                return contains(x.inst)
            elif isinstance(x, (hm.TNom, hm.TFresh)):
                return False
            else:
                assert isinstance(x, hm.TVar)
                if i == x.i: return True
                var = self.load_tvar(x.i)
                if var == x:
                    return False
                return contains(var)

        return contains(hmt)

    def free(self, fresh_map: t.Dict[str, hm.HMT], to_fresh: hm.HMT):
        def mk_free(x: hm.HMT):
            if isinstance(x, (hm.TNom, hm.TVar)):
                return x
            if isinstance(x, hm.TApp):
                return hm.TApp(mk_free(x.fn), mk_free(x.arg))
            if isinstance(x, hm.TArrow):
                return hm.TArrow(mk_free(x.dom), mk_free(x.codom))
            if isinstance(x, hm.TTup):
                return hm.TTup(tuple(map(mk_free, x.elts)))
            if isinstance(x, hm.TFresh):
                return fresh_map.get(x.s, x)

            assert isinstance(x, hm.TForall)
            freshs = x.vars
            new_fresh_map = {
                k: v
                for k, v in fresh_map.items() if k not in freshs
            }
            return hm.TForall(freshs, self.free(new_fresh_map, x.inst))

        return mk_free(to_fresh)

    def prune(self, x: hm.HMT):
        if isinstance(x, (hm.TFresh, hm.TNom)):
            return x
        if isinstance(x, hm.TForall):
            return hm.TForall(x.vars, self.prune(x.inst))
        if isinstance(x, hm.TApp):
            return hm.TApp(self.prune(x.fn), self.prune(x.arg))
        if isinstance(x, hm.TArrow):
            return hm.TArrow(self.prune(x.dom), self.prune(x.codom))
        if isinstance(x, hm.TTup):
            return hm.TTup(tuple(map(self.prune, x.elts)))

        assert isinstance(x, hm.TVar)
        i = x.i
        v = self.load_tvar(i)
        if isinstance(v, hm.TVar) and v.i == i:
            return x
        v = self.tvars[i] = self.prune(v)
        return v

    def add_neq(self, l: hm.HMT, r: hm.HMT):
        lr = tuple(sorted((l, r)))
        self.neqs.add(lr)

    def unify(self, unif: 'HMUnify'):
        if not unif.is_pos:
            self.add_neq(unif.l, unif.r)
        else:
            self._unify_root(unif.l, unif.r)

    def _unify_root(self, l, r):
        l = self.prune(l)
        r = self.prune(r)

        def unify_rec(l, r):
            if isinstance(l, hm.TForall):
                free_map = {v: self.new_tvar() for v in l.vars}
                inst = self.free(free_map, l.inst)
                return self._unify_root(inst, r)
            if isinstance(r, hm.TForall):
                return unify_rec(r, l)
            if isinstance(l, hm.TNom) and isinstance(r, hm.TNom):
                return l.nom == r.nom
            if isinstance(l, hm.TVar) and isinstance(r, hm.TVar):
                if l.i == r.i:
                    return True
                if self.occur_in(l.i, r):
                    raise TypeError(
                        "Ill-formed type definition like a = a -> b")

                self.tvars[l.i] = r
                return True
            if isinstance(l, hm.TVar):
                self.tvars[l.i] = r
                return True
            if isinstance(r, hm.TVar):
                return unify_rec(r, l)
            if isinstance(l, hm.TApp) and isinstance(r, hm.TApp):
                return self._unify_root(l.fn, r.fn) and self._unify_root(
                    l.arg, r.arg)
            if isinstance(l, hm.TArrow) and isinstance(r, hm.TArrow):
                return self._unify_root(l.dom, r.dom) and self._unify_root(
                    l.codom, r.codom)

            if isinstance(l, hm.TTup) and isinstance(r, hm.TTup):
                if len(l.elts) != len(r.elts):
                    return False
                return all(
                    self._unify_root(a1, a2) for a1, a2 in zip(l.elts, r.elts))

            raise TypeError(f"{l} ? {r}")

        return unify_rec(l, r)


@dataclass(frozen=True, order=True)
class HMUnify:
    l: hm.HMT
    r: hm.HMT
    is_pos: bool = True

    def not_a(self):
        return [HMUnify(self.l, self.r, is_pos=not self.is_pos)]
