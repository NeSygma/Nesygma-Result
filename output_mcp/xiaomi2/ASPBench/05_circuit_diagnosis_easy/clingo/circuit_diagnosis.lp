% Circuit Diagnosis Problem - Find all minimal sets of faulty components

% ===== DOMAIN DEFINITIONS =====
% Gate definitions: gate(Name, Type, Input1, Input2, Output)
gate(and1, and, in1, in2, w1).
gate(or1, or, w1, in3, w2).
gate(ngate1, neg, w2, none, out1).
gate(xor1, xor, in1, in4, w3).
gate(and2, and, w3, in2, out2).

% Input values for test case
input(in1, 1).
input(in2, 0).
input(in3, 1).
input(in4, 1).

% Observed outputs
observed(out1, 1).
observed(out2, 0).

% All wires
wire(in1). wire(in2). wire(in3). wire(in4).
wire(w1). wire(w2). wire(w3).
wire(out1). wire(out2).

% ===== CHOICE RULES =====
% Each gate can be faulty or not
{ faulty(G) } :- gate(G, _, _, _, _).

% ===== WIRE VALUE PROPAGATION =====
% Input wires have fixed values
value(W, V) :- input(W, V).

% Working gate definition
working(G) :- gate(G, _, _, _, _), not faulty(G).

% AND gate: output = 1 iff both inputs are 1
value(Out, 1) :- gate(G, and, In1, In2, Out), value(In1, 1), value(In2, 1), working(G).
value(Out, 0) :- gate(G, and, In1, In2, Out), value(In1, 0), working(G).
value(Out, 0) :- gate(G, and, In1, In2, Out), value(In2, 0), working(G).

% OR gate: output = 1 iff at least one input is 1
value(Out, 1) :- gate(G, or, In1, In2, Out), value(In1, 1), working(G).
value(Out, 1) :- gate(G, or, In1, In2, Out), value(In2, 1), working(G).
value(Out, 0) :- gate(G, or, In1, In2, Out), value(In1, 0), value(In2, 0), working(G).

% NOT gate: output = 1 iff input is 0
value(Out, 1) :- gate(G, neg, In, _, Out), value(In, 0), working(G).
value(Out, 0) :- gate(G, neg, In, _, Out), value(In, 1), working(G).

% XOR gate: output = 1 iff exactly one input is 1
value(Out, 1) :- gate(G, xor, In1, In2, Out), value(In1, 0), value(In2, 1), working(G).
value(Out, 1) :- gate(G, xor, In1, In2, Out), value(In1, 1), value(In2, 0), working(G).
value(Out, 0) :- gate(G, xor, In1, In2, Out), value(In1, 0), value(In2, 0), working(G).
value(Out, 0) :- gate(G, xor, In1, In2, Out), value(In1, 1), value(In2, 1), working(G).

% For faulty gates, output can be either 0 or 1 (non-deterministic)
{ value(Out, 0); value(Out, 1) } = 1 :- gate(G, _, _, _, Out), faulty(G).

% ===== CONSTRAINTS =====
% Each wire must have exactly one value
:- value(W, V1), value(W, V2), V1 != V2.

% Observed outputs must match
:- observed(W, V), not value(W, V).

% ===== MINIMALITY =====
% Minimize the number of faulty gates
#minimize { 1,G : faulty(G) }.

% ===== OUTPUT =====
#show faulty/1.