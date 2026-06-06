from z3 import *

# Define gates data
# Each gate: name, type, inputs (list), output wire
gates = [
    # Layer 1
    ('and1', 'AND', ['in1','in2'], 'w1'),
    ('xor1', 'XOR', ['in3','in4'], 'w2'),
    ('or1', 'OR', ['in5','in6'], 'w3'),
    ('and2', 'AND', ['in7','in8'], 'w4'),
    ('xor2', 'XOR', ['in9','in10'], 'w5'),
    ('not1', 'NOT', ['in1'], 'w6'),
    ('or2', 'OR', ['in3','in5'], 'w7'),
    ('and3', 'AND', ['in4','in6'], 'w8'),
    # Layer 2
    ('and4', 'AND', ['w1','w2'], 'w9'),
    ('or3', 'OR', ['w3','w4'], 'w10'),
    ('xor4', 'XOR', ['w5','w6'], 'w11'),
    ('and5', 'AND', ['w2','w7'], 'w12'),
    ('or4', 'OR', ['w8','w5'], 'w13'),
    ('not2', 'NOT', ['w7'], 'w14'),
    ('xor5', 'XOR', ['w6','w1'], 'w15'),
    ('and6', 'AND', ['w4','w8'], 'w16'),
    # Layer 3
    ('xor6', 'XOR', ['w9','w10'], 'w17'),
    ('and7', 'AND', ['w11','w12'], 'w18'),
    ('or5', 'OR', ['w13','w14'], 'w19'),
    ('xor7', 'XOR', ['w15','w16'], 'w20'),
    ('and8', 'AND', ['w9','w13'], 'w21'),
    ('or6', 'OR', ['w10','w12'], 'w22'),
    ('not3', 'NOT', ['w11'], 'w23'),
    ('xor8', 'XOR', ['w14','w16'], 'w24'),
    # Layer 4
    ('and9', 'AND', ['w17','w18'], 'w25'),
    ('or7', 'OR', ['w19','w20'], 'w26'),
    ('xor9', 'XOR', ['w21','w22'], 'w27'),
    ('and10', 'AND', ['w23','w24'], 'w28'),
    ('or8', 'OR', ['w25','w26'], 'w29'),
    ('xor10', 'XOR', ['w27','w28'], 'w30'),
    ('and11', 'AND', ['w22','w24'], 'w31'),
    ('or9', 'OR', ['w21','w23'], 'w32'),
    # Final Stage
    ('xor11', 'XOR', ['w29','w30'], 'u1'),
    ('and12', 'AND', ['w31','w32'], 'u2'),
    ('or10', 'OR', ['w17','w29'], 'u3'),
    ('not4', 'NOT', ['u2'], 'out2'),
    ('or11', 'OR', ['u1','u3'], 'out1'),
    ('xor12', 'XOR', ['w30','w31'], 'out3'),
]

# Map output wire to gate name
wire_to_gate = {out: name for (name,_,_,out) in gates}

# Test vectors and observed outputs
tests = [
    ({'in1':1,'in2':1,'in3':0,'in4':1,'in5':1,'in6':0,'in7':1,'in8':0,'in9':1,'in10':0}, (0,1,0)),
    ({'in1':0,'in2':1,'in3':1,'in4':0,'in5':1,'in6':1,'in7':0,'in8':1,'in9':1,'in10':1}, (0,1,0)),
    ({'in1':1,'in2':0,'in3':1,'in4':1,'in5':0,'in6':0,'in7':1,'in8':1,'in9':0,'in10':0}, (0,1,0)),
    ({'in1':0,'in2':0,'in3':0,'in4':1,'in5':1,'in6':1,'in7':1,'in8':0,'in9':0,'in10':1}, (0,1,0)),
    ({'in1':1,'in2':1,'in3':1,'in4':1,'in5':0,'in6':1,'in7':0,'in8':0,'in9':1,'in10':0}, (0,1,0)),
    ({'in1':0,'in2':1,'in3':0,'in4':0,'in5':1,'in6':0,'in7':1,'in8':1,'in9':0,'in10':1}, (0,1,0)),
    ({'in1':1,'in2':0,'in3':0,'in4':1,'in5':0,'in6':1,'in7':1,'in8':0,'in9':1,'in10':1}, (0,1,0)),
    ({'in1':0,'in2':0,'in3':1,'in4':0,'in5':1,'in6':0,'in7':0,'in8':1,'in9':1,'in10':0}, (0,1,0)),
]

opt = Optimize()

# Fault mode per gate: 0=none,1=stuck0,2=stuck1,3=invert,4=open
fault_vars = {}
for name,_,_,_ in gates:
    fv = Int(f"fault_{name}")
    fault_vars[name] = fv
    opt.add(fv >= 0, fv <= 4)

# Cost expression
costs = []
fault_counts = []
for name in fault_vars:
    fv = fault_vars[name]
    cost = If(fv == 0, 0, If(fv == 4, 2, 1))
    costs.append(cost)
    fault_counts.append(If(fv != 0, 1, 0))
opt.add(Sum(fault_counts) <= 3)

total_cost = Sum(costs)
opt.minimize(total_cost)

# Create output variables per gate per test
out_vars = {}  # (gate, test_index) -> Bool
for ti, (inp_dict, _) in enumerate(tests):
    for name, _, _, _ in gates:
        out_vars[(name, ti)] = Bool(f"out_{name}_{ti}")

# Helper to get Bool for a wire in a given test
def wire_bool(wire, ti, inp_dict):
    if wire.startswith('in'):
        return BoolVal(bool(inp_dict[wire]))
    else:
        # find gate that produces this wire
        gate = wire_to_gate[wire]
        return out_vars[(gate, ti)]

# Add constraints for each gate and each test
for ti, (inp_dict, _) in enumerate(tests):
    for (gname, gtype, inputs, outwire) in gates:
        out_var = out_vars[(gname, ti)]
        # compute correct expression based on inputs (using actual outputs of predecessor gates)
        in_exprs = [wire_bool(w, ti, inp_dict) for w in inputs]
        if gtype == 'AND':
            correct = And(*in_exprs)
        elif gtype == 'OR':
            correct = Or(*in_exprs)
        elif gtype == 'XOR':
            # Z3 Xor works for any number of args
            correct = Xor(*in_exprs)
        elif gtype == 'NOT':
            correct = Not(in_exprs[0])
        else:
            raise Exception('unknown type')
        fv = fault_vars[gname]
        # Constraint linking fault mode to output
        opt.add(Or(
            And(fv == 0, out_var == correct),
            And(fv == 1, out_var == False),
            And(fv == 2, out_var == True),
            And(fv == 3, out_var == Not(correct)),
            fv == 4  # open, no restriction on out_var
        ))

# Observed outputs constraints
for ti, (_, (obs1, obs2, obs3)) in enumerate(tests):
    # out1 from gate or11, out2 from not4, out3 from xor12
    opt.add(out_vars[('or11', ti)] == BoolVal(bool(obs1)))
    opt.add(out_vars[('not4', ti)] == BoolVal(bool(obs2)))
    opt.add(out_vars[('xor12', ti)] == BoolVal(bool(obs3)))

# Solve
res = opt.check()
if res == sat:
    m = opt.model()
    print("STATUS: sat")
    total = m.evaluate(total_cost).as_long()
    print("total_cost =", total)
    # list faulty components
    for name in fault_vars:
        fv = m.evaluate(fault_vars[name]).as_long()
        if fv != 0:
            mode = {1:'stuck0',2:'stuck1',3:'invert',4:'open'}.get(fv, 'unknown')
            print(f"fault: {name} mode={mode}")
else:
    print("STATUS: unsat")