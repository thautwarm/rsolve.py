from rsolve.hm.unification import TCEnv, HMUnify
from rsolve.hm.hm import *
from rsolve.hm.nominal import *
print('running test_hm.py')
# t1 == t2 && t1 == int32
# =>
# t1 = t2 = int32
env = TCEnv(None)
t1 = env.new_tvar()
t2 = env.new_tvar()
eq = HMUnify(t1, t2)
inst = HMUnify(t1, TNom(Int(32)))
env.unify(eq)
env.unify(inst)
assert env.prune(t2) == TNom(Int(32))

# t1 == (t2, t2) && t1 == t3 && t3 == (text32, t4)
# =>
# t1 = t3 = (text32, text32)
# t2 = t4 = text32
text32 = TNom(Text(32))
env = TCEnv(None)
t1 = env.new_tvar()
t2 = env.new_tvar()
t3 = env.new_tvar()
t4 = env.new_tvar()
eq1 = HMUnify(t1, TTup((t2, t2)))
eq2 = HMUnify(t1, t3)
eq3 = HMUnify(t3, TTup((text32, t4)))

for eq in [eq1, eq2, eq3]:
    env.unify(eq)

assert env.prune(t1) == TTup((text32, text32))
assert env.prune(t2) == text32
assert env.prune(t3) == TTup((text32, text32))
assert env.prune(t4) == text32
