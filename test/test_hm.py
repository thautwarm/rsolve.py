from rsolve.hm.unification import TCEnv, HMUnify
from rsolve.hm.hm import *
from rsolve.hm.nominal import *

env = TCEnv(None)

t1 = env.new_tvar()
t2 = env.new_tvar()

eq = HMUnify(t1, t2)
inst = HMUnify(t1, TNom(Int(32)))

env.unify(eq)

env.unify(inst)

assert env.prune(t1) == TNom(Int(32))
