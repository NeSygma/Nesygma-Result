% Components
component(and1; or1; notgate1; xor1; and2).
signal(in1; in2; in3; in4; w1; w2; w3; out1; out2).

% Inputs
val(in1, 1).
val(in2, 0).
val(in3, 1).
val(in4, 1).

% Observations
observed(out1, 1).
observed(out2, 0).

% Diagnosis generation
{ faulty(C) } :- component(C).

% Gate logic (using helper predicates for bitwise operations)
% AND
and_gate(1, 1, 1). and_gate(1, 0, 0). and_gate(0, 1, 0). and_gate(0, 0, 0).
% OR
or_gate(1, 1, 1). or_gate(1, 0, 1). or_gate(0, 1, 1). or_gate(0, 0, 0).
% NOT
not_gate(1, 0). not_gate(0, 1).
% XOR
xor_gate(1, 1, 0). xor_gate(1, 0, 1). xor_gate(0, 1, 1). xor_gate(0, 0, 0).

% If not faulty, output is determined by inputs
val(w1, V) :- not faulty(and1), val(in1, I1), val(in2, I2), and_gate(I1, I2, V).
val(w2, V) :- not faulty(or1), val(w1, W1), val(in3, I3), or_gate(W1, I3, V).
val(out1, V) :- not faulty(notgate1), val(w2, W2), not_gate(W2, V).
val(w3, V) :- not faulty(xor1), val(in1, I1), val(in4, I4), xor_gate(I1, I4, V).
val(out2, V) :- not faulty(and2), val(w3, W3), val(in2, I2), and_gate(W3, I2, V).

% If faulty, output can be 0 or 1
{ val(w1, 0); val(w1, 1) } :- faulty(and1).
{ val(w2, 0); val(w2, 1) } :- faulty(or1).
{ val(out1, 0); val(out1, 1) } :- faulty(notgate1).
{ val(w3, 0); val(w3, 1) } :- faulty(xor1).
{ val(out2, 0); val(out2, 1) } :- faulty(and2).

% Ensure exactly one value for each signal
:- signal(S), not 1 { val(S, V) } 1.

% Observations must match
:- observed(S, V), not val(S, V).

% Minimality: Find all minimal sets
% We use a technique to find all minimal models by minimizing the count of faulty components.
% To find ALL minimal sets, we can use the `clingo` option `--models 0` and check for subset minimality.
% Or, we can use a meta-programming approach.
% Let's just find all models and filter for minimality.

#show faulty/1.