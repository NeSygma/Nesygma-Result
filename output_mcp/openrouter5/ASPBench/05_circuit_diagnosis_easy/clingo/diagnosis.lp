% --- Circuit Components ---
component(and1; or1; notgate1; xor1; and2).

% --- Gate Types ---
gate_type(and1, and).
gate_type(or1, or).
gate_type(notgate1, not).
gate_type(xor1, xor).
gate_type(and2, and).

% --- Connections ---
% and1: inputs in1, in2 -> output w1
conn(and1, in1, in1).
conn(and1, in2, in2).
conn(and1, out, w1).

% or1: inputs w1, in3 -> output w2
conn(or1, in1, w1).
conn(or1, in2, in3).
conn(or1, out, w2).

% notgate1: input w2 -> output out1
conn(notgate1, in, w2).
conn(notgate1, out, out1).

% xor1: inputs in1, in4 -> output w3
conn(xor1, in1, in1).
conn(xor1, in2, in4).
conn(xor1, out, w3).

% and2: inputs w1, in2 -> output out2
conn(and2, in1, w3).
conn(and2, in2, in2).
conn(and2, out, out2).

% --- Input Values ---
input_val(in1, 1).
input_val(in2, 0).
input_val(in3, 1).
input_val(in4, 1).

% --- Expected Outputs (if all working) ---
expected(out1, 0).
expected(out2, 0).

% --- Observed Outputs ---
observed(out1, 1).
observed(out2, 0).

% --- Wire/Line domain ---
wire(in1; in2; in3; in4; w1; w2; w3; out1; out2).

% --- Diagnosis: choose which components are faulty ---
{ faulty(C) } :- component(C).

% --- For each wire, determine its value ---
% Primary inputs get their input values
wire_val(W, V) :- input_val(W, V).

% For each component that is NOT faulty, compute output normally
% AND gate
wire_val(Out, V) :- 
    component(C), gate_type(C, and), 
    conn(C, out, Out),
    not faulty(C),
    conn(C, in1, In1), wire_val(In1, V1),
    conn(C, in2, In2), wire_val(In2, V2),
    V = V1 * V2.

% OR gate
wire_val(Out, V) :-
    component(C), gate_type(C, or),
    conn(C, out, Out),
    not faulty(C),
    conn(C, in1, In1), wire_val(In1, V1),
    conn(C, in2, In2), wire_val(In2, V2),
    V = (V1 + V2) - (V1 * V2).

% NOT gate
wire_val(Out, V) :-
    component(C), gate_type(C, not),
    conn(C, out, Out),
    not faulty(C),
    conn(C, in, In), wire_val(In, Vi),
    V = 1 - Vi.

% XOR gate
wire_val(Out, V) :-
    component(C), gate_type(C, xor),
    conn(C, out, Out),
    not faulty(C),
    conn(C, in1, In1), wire_val(In1, V1),
    conn(C, in2, In2), wire_val(In2, V2),
    V = (V1 + V2) - 2*V1*V2.

% For faulty components, the output wire can be either 0 or 1
{ wire_val(W, 0) } :- component(C), conn(C, out, W), faulty(C).
{ wire_val(W, 1) } :- component(C), conn(C, out, W), faulty(C).

% --- Constraints ---
% Each wire must have exactly one value
:- wire(W), #count { V : wire_val(W, V) } != 1.

% Observed outputs must match
:- observed(W, V), not wire_val(W, V).

% --- Find all diagnoses ---
% Show the faulty components in each diagnosis
#show faulty/1.