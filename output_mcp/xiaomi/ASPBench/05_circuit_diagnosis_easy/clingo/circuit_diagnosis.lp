% Circuit Diagnosis Problem - Find all minimal sets of faulty components

% Components (gates)
gate(and1). gate(or1). gate(notgate1). gate(xor1). gate(and2).

% Input values (fixed)
input(in1, 1). input(in2, 0). input(in3, 1). input(in4, 1).

% Wire connections: gate, input wires, output wire
gate_inputs(and1, in1). gate_inputs(and1, in2). gate_output(and1, w1).
gate_inputs(or1, w1). gate_inputs(or1, in3). gate_output(or1, w2).
gate_inputs(notgate1, w2). gate_output(notgate1, out1).
gate_inputs(xor1, in1). gate_inputs(xor1, in4). gate_output(xor1, w3).
gate_inputs(and2, w3). gate_inputs(and2, in2). gate_output(and2, out2).

% Gate types
gate_type(and1, and). gate_type(or1, or). gate_type(notgate1, not).
gate_type(xor1, xor). gate_type(and2, and).

% Observed outputs
observed(out1, 1). observed(out2, 0).

% Wire values - either from inputs or gate outputs
% Input wires have fixed values
wire_value(W, V) :- input(W, V).

% Choice: each gate can be faulty or working
{ faulty(G) } :- gate(G).

% For AND gate: output = 1 iff both inputs are 1
wire_value(W, 1) :- gate(G), gate_type(G, and), gate_output(G, W), 
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, 1),
                     gate_inputs(G, W2), wire_value(W2, 1), W1 != W2.

wire_value(W, 0) :- gate(G), gate_type(G, and), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, 0).

wire_value(W, 0) :- gate(G), gate_type(G, and), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W2), wire_value(W2, 0).

% For OR gate: output = 1 iff at least one input is 1
wire_value(W, 1) :- gate(G), gate_type(G, or), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, 1).

wire_value(W, 0) :- gate(G), gate_type(G, or), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, 0),
                     gate_inputs(G, W2), wire_value(W2, 0), W1 != W2.

% For NOT gate: output = opposite of input
wire_value(W, 0) :- gate(G), gate_type(G, not), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, 1).

wire_value(W, 1) :- gate(G), gate_type(G, not), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, 0).

% For XOR gate: output = 1 iff inputs differ
wire_value(W, 1) :- gate(G), gate_type(G, xor), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, V1),
                     gate_inputs(G, W2), wire_value(W2, V2), V1 != V2.

wire_value(W, 0) :- gate(G), gate_type(G, xor), gate_output(G, W),
                     not faulty(G),
                     gate_inputs(G, W1), wire_value(W1, V1),
                     gate_inputs(G, W2), wire_value(W2, V2), V1 == V2.

% If gate is faulty, its output can be anything (0 or 1)
{ wire_value(W, 0..1) } :- gate(G), faulty(G), gate_output(G, W).

% Constraint: observed outputs must match wire values
:- observed(W, V), not wire_value(W, V).

% We want to find all diagnoses (sets of faulty gates)
% A diagnosis is valid if it explains the observations
diagnosis(F) :- faulty(F).

% Count the number of faulty gates
faulty_count(N) :- N = #count{F : faulty(F)}.

% We want minimal diagnoses - use optimization to minimize faulty gates
#minimize { 1,F : faulty(F) }.

% Show the faulty gates
#show diagnosis/1.
#show faulty_count/1.