% Components
component(and1).
component(or1).
component(notgate1).
component(xor1).
component(and2).

% Input values (as base facts)
val(in1,1).
val(in2,0).
val(in3,1).
val(in4,1).

% Choice of faulty components (diagnosis)
{ faulty(C) } :- component(C).

% Exclusivity: each wire has at most one value
:- val(W,0), val(W,1).
:- val_t(W,0), val_t(W,1).

% ---------- Main circuit (using faulty set) ----------
% AND gate and1 -> w1
val(w1,1) :- val(in1,1), val(in2,1), not faulty(and1).
val(w1,0) :- (val(in1,0); val(in2,0)), not faulty(and1).
% OR gate or1 -> w2
val(w2,1) :- (val(w1,1); val(in3,1)), not faulty(or1).
val(w2,0) :- val(w1,0), val(in3,0), not faulty(or1).
% NOT gate notgate1 -> out1
val(out1,1) :- val(w2,0), not faulty(notgate1).
val(out1,0) :- val(w2,1), not faulty(notgate1).
% XOR gate xor1 -> w3
val(w3,1) :- val(in1,1), val(in4,0), not faulty(xor1).
val(w3,1) :- val(in1,0), val(in4,1), not faulty(xor1).
val(w3,0) :- val(in1,1), val(in4,1), not faulty(xor1).
val(w3,0) :- val(in1,0), val(in4,0), not faulty(xor1).
% AND gate and2 -> out2
val(out2,1) :- val(w3,1), val(in2,1), not faulty(and2).
val(out2,0) :- (val(w3,0); val(in2,0)), not faulty(and2).

% Faulty components can produce any value on their output wire (exactly one)
1 { val(w1,0); val(w1,1) } 1 :- faulty(and1).
1 { val(w2,0); val(w2,1) } 1 :- faulty(or1).
1 { val(out1,0); val(out1,1) } 1 :- faulty(notgate1).
1 { val(w3,0); val(w3,1) } 1 :- faulty(xor1).
1 { val(out2,0); val(out2,1) } 1 :- faulty(and2).

% Observation constraints (must match observed outputs)
:- not val(out1,1).
:- not val(out2,0).

% ---------- Minimality check ----------
% For each faulty component we may try to exclude it and see if observations still hold.
{ exclude(C) } :- faulty(C).
% Define test faulty set (faulty components after exclusion)
faulty_test(C) :- faulty(C), not exclude(C).

% Input values for test copy
val_t(in1,1). val_t(in2,0). val_t(in3,1). val_t(in4,1).

% Deterministic behavior for test copy (using faulty_test)
val_t(w1,1) :- val_t(in1,1), val_t(in2,1), not faulty_test(and1).
val_t(w1,0) :- (val_t(in1,0); val_t(in2,0)), not faulty_test(and1).
val_t(w2,1) :- (val_t(w1,1); val_t(in3,1)), not faulty_test(or1).
val_t(w2,0) :- val_t(w1,0), val_t(in3,0), not faulty_test(or1).
val_t(out1,1) :- val_t(w2,0), not faulty_test(notgate1).
val_t(out1,0) :- val_t(w2,1), not faulty_test(notgate1).
val_t(w3,1) :- val_t(in1,1), val_t(in4,0), not faulty_test(xor1).
val_t(w3,1) :- val_t(in1,0), val_t(in4,1), not faulty_test(xor1).
val_t(w3,0) :- val_t(in1,1), val_t(in4,1), not faulty_test(xor1).
val_t(w3,0) :- val_t(in1,0), val_t(in4,0), not faulty_test(xor1).
val_t(out2,1) :- val_t(w3,1), val_t(in2,1), not faulty_test(and2).
val_t(out2,0) :- (val_t(w3,0); val_t(in2,0)), not faulty_test(and2).

% Faulty_test components can produce any value on their output wire
1 { val_t(w1,0); val_t(w1,1) } 1 :- faulty_test(and1).
1 { val_t(w2,0); val_t(w2,1) } 1 :- faulty_test(or1).
1 { val_t(out1,0); val_t(out1,1) } 1 :- faulty_test(notgate1).
1 { val_t(w3,0); val_t(w3,1) } 1 :- faulty_test(xor1).
1 { val_t(out2,0); val_t(out2,1) } 1 :- faulty_test(and2).

% Observation must hold in test copy as well
obs_ok_t :- val_t(out1,1), val_t(out2,0).
:- not obs_ok_t.

% If we can exclude a faulty component and still satisfy observations, then original set is not minimal
:- exclude(C), obs_ok_t.

#show faulty/1.