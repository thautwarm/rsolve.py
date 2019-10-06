from rsolve.hm.unification import TCEnv, HMUnify
from rsolve.hm.hm import *
from rsolve.hm.nominal import *
print('running test_hm.py')
# t1 == t2 && t1 == int32
# =>
# t1 = t2 = int32
int32 = TNom(Int(32))
env = TCEnv(None)
t1 = env.new_tvar()
t2 = env.new_tvar()
eq = HMUnify(t1, t2)
inst = HMUnify(t1, int32)
env.unify(eq)
env.unify(inst)
assert env.prune(t2) == int32

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

# # x1 == exist a b. (a, b) && x1 == x3 &&
# # x3 == exist a. (text32, exist a. a) && x3 == exist a . (a, int32)
# # =>
# # x1 = x3 = (text32, int32)
# text32 = TNom(Text(32))
# env = TCEnv(None)
# x1 = env.new_tvar()
# x3 = env.new_tvar()
#
# eq1 = HMUnify(x1,
#               TExist(frozenset(["a", "b"]), TTup((TFresh("a"), TFresh("b")))))
# eq2 = HMUnify(x1, x3)
# eq3 = HMUnify(x3, TExist(frozenset(["a"]), TTup((int32, TFresh("a")))))
# eq4 = HMUnify(x3, TExist(frozenset(["a"]), TTup((TFresh("a"), text32))))
#
# for eq in [eq1, eq2, eq3, eq4]:
#     env.unify(eq)
#
# assert env.prune(x1) == TTup((int32, text32)) == env.prune(x3)
