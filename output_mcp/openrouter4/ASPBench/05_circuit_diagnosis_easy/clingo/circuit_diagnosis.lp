% ----- Circuit Diagnosis Problem -----
% Find all minimal sets of faulty components that explain observed outputs.

% ----- Domain Definitions -----
component(and1; or1; notgate1; xor1; and2).

gate_type(and1, and_gate). gate_type(or1, or_gate). 
gate_type(notgate1, not_gate). gate_type(xor1, xor_gate). gate_type(and2, and_gate).

% Output wire for each component
out_wire(and1, w1). out_wire(or1, w2). out_wire(notgate1, out1). out_wire(xor1, w3). out_wire(and2, out2).

% Input connections per component
in_wire(and1, in1). in_wire(and1, in2).
in_wire(or1, w1). in_wire(or1, in3).
in_wire(notgate1, w2).
in_wire(xor1, in1). in_wire(xor1, in4).
in_wire(and2, w3). in_wire(and2, in2).

% All wires
wire(in1; in2; in3; in4; w1; w2; w3; out1; out2).

% Input values (test case)
input_val(in1, 1). input_val(in2, 0). input_val(in3, 1). input_val(in4, 1).

% Observed output values
observed(out1, 1). observed(out2, 0).

% ----- Diagnosis Generation -----
% Each component may be faulty
{ faulty(C) } :- component(C).

% Wire values: each wire (except inputs) gets exactly one value
1 { wire_val(W, 0); wire_val(W, 1) } 1 :- wire(W), W != in1, W != in2, W != in3, W != in4.

% Input wire values are fixed
wire_val(W, V) :- input_val(W, V).

% ----- Working Component Behavior -----
% AND gate: output=1 iff both inputs=1
wire_val(W, 1) :- out_wire(C, W), not faulty(C), gate_type(C, and_gate),
                  in_wire(C, I1), in_wire(C, I2), I1 != I2,
                  wire_val(I1, 1), wire_val(I2, 1).
wire_val(W, 0) :- out_wire(C, W), not faulty(C), gate_type(C, and_gate),
                  in_wire(C, I1), in_wire(C, I2), I1 != I2,
                  { wire_val(I1, 0); wire_val(I2, 0) }.

% OR gate: output=0 iff both inputs=0
wire_val(W, 0) :- out_wire(C, W), not faulty(C), gate_type(C, or_gate),
                  in_wire(C, I1), in_wire(C, I2), I1 != I2,
                  wire_val(I1, 0), wire_val(I2, 0).
wire_val(W, 1) :- out_wire(C, W), not faulty(C), gate_type(C, or_gate),
                  in_wire(C, I1), in_wire(C, I2), I1 != I2,
                  { wire_val(I1, 1); wire_val(I2, 1) }.

% NOT gate: output=1 iff input=0
wire_val(W, 1) :- out_wire(C, W), not faulty(C), gate_type(C, not_gate),
                  in_wire(C, I), wire_val(I, 0).
wire_val(W, 0) :- out_wire(C, W), not faulty(C), gate_type(C, not_gate),
                  in_wire(C, I), wire_val(I, 1).

% XOR gate: output=1 iff inputs differ
wire_val(W, 1) :- out_wire(C, W), not faulty(C), gate_type(C, xor_gate),
                  in_wire(C, I1), in_wire(C, I2), I1 != I2,
                  wire_val(I1, V1), wire_val(I2, V2), V1 != V2.
wire_val(W, 0) :- out_wire(C, W), not faulty(C), gate_type(C, xor_gate),
                  in_wire(C, I1), in_wire(C, I2), I1 != I2,
                  wire_val(I1, V1), wire_val(I2, V2), V1 == V2.

% ----- Observations Constraint -----
% Observed output values must match
:- observed(W, V), not wire_val(W, V).

% ----- Minimality Check -----
% A diagnosis is a set of faulty components that satisfies observations.
% A diagnosis is minimal if no proper subset is also a diagnosis.
% 
% For each faulty component C, we check if removing C (making it working)
% while keeping other faulty components as-is still allows observations to be satisfied.
% If removal is possible, the current set is NOT minimal.

% For the removal check of component C, we define alt_val(C, W, V) as wire values
% in the scenario where C is forced to be working.

% Generate alternative wire values for each removal scenario
1 { alt_val(C, W, 0); alt_val(C, W, 1) } 1 :- component(C), wire(W), 
    W != in1, W != in2, W != in3, W != in4.

% Input values are the same in all scenarios
alt_val(C, W, V) :- component(C), input_val(W, V).

% Working components (except C, which is always working in its own scenario)
% For components that are not C: they keep their original faulty status
% For component C: it is always working

% AND gate behavior in removal scenario
alt_val(C, W, 1) :- component(C), out_wire(C2, W), gate_type(C2, and_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I1), in_wire(C2, I2), I1 != I2,
                    alt_val(C, I1, 1), alt_val(C, I2, 1).
alt_val(C, W, 0) :- component(C), out_wire(C2, W), gate_type(C2, and_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I1), in_wire(C2, I2), I1 != I2,
                    { alt_val(C, I1, 0); alt_val(C, I2, 0) }.

% C itself working (AND gate)
alt_val(C, W, 1) :- component(C), out_wire(C, W), gate_type(C, and_gate),
                    in_wire(C, I1), in_wire(C, I2), I1 != I2,
                    alt_val(C, I1, 1), alt_val(C, I2, 1).
alt_val(C, W, 0) :- component(C), out_wire(C, W), gate_type(C, and_gate),
                    in_wire(C, I1), in_wire(C, I2), I1 != I2,
                    { alt_val(C, I1, 0); alt_val(C, I2, 0) }.

% OR gate behavior in removal scenario
alt_val(C, W, 0) :- component(C), out_wire(C2, W), gate_type(C2, or_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I1), in_wire(C2, I2), I1 != I2,
                    alt_val(C, I1, 0), alt_val(C, I2, 0).
alt_val(C, W, 1) :- component(C), out_wire(C2, W), gate_type(C2, or_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I1), in_wire(C2, I2), I1 != I2,
                    { alt_val(C, I1, 1); alt_val(C, I2, 1) }.

% C itself working (OR gate)
alt_val(C, W, 0) :- component(C), out_wire(C, W), gate_type(C, or_gate),
                    in_wire(C, I1), in_wire(C, I2), I1 != I2,
                    alt_val(C, I1, 0), alt_val(C, I2, 0).
alt_val(C, W, 1) :- component(C), out_wire(C, W), gate_type(C, or_gate),
                    in_wire(C, I1), in_wire(C, I2), I1 != I2,
                    { alt_val(C, I1, 1); alt_val(C, I2, 1) }.

% NOT gate behavior in removal scenario
alt_val(C, W, 1) :- component(C), out_wire(C2, W), gate_type(C2, not_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I), alt_val(C, I, 0).
alt_val(C, W, 0) :- component(C), out_wire(C2, W), gate_type(C2, not_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I), alt_val(C, I, 1).

% C itself working (NOT gate)
alt_val(C, W, 1) :- component(C), out_wire(C, W), gate_type(C, not_gate),
                    in_wire(C, I), alt_val(C, I, 0).
alt_val(C, W, 0) :- component(C), out_wire(C, W), gate_type(C, not_gate),
                    in_wire(C, I), alt_val(C, I, 1).

% XOR gate behavior in removal scenario
alt_val(C, W, 1) :- component(C), out_wire(C2, W), gate_type(C2, xor_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I1), in_wire(C2, I2), I1 != I2,
                    alt_val(C, I1, V1), alt_val(C, I2, V2), V1 != V2.
alt_val(C, W, 0) :- component(C), out_wire(C2, W), gate_type(C2, xor_gate),
                    C2 != C, not faulty(C2),
                    in_wire(C2, I1), in_wire(C2, I2), I1 != I2,
                    alt_val(C, I1, V1), alt_val(C, I2, V2), V1 == V2.

% C itself working (XOR gate)
alt_val(C, W, 1) :- component(C), out_wire(C, W), gate_type(C, xor_gate),
                    in_wire(C, I1), in_wire(C, I2), I1 != I2,
                    alt_val(C, I1, V1), alt_val(C, I2, V2), V1 != V2.
alt_val(C, W, 0) :- component(C), out_wire(C, W), gate_type(C, xor_gate),
                    in_wire(C, I1), in_wire(C, I2), I1 != I2,
                    alt_val(C, I1, V1), alt_val(C, I2, V2), V1 == V2.

% For faulty components (other than C), their outputs are free in the removal scenario
% This is already covered by the choice rule for alt_val that allows any value.

% But we need to ensure that faulty components (other than C) are NOT constrained
% by the working gate rules. We need to prevent the working gate rules from applying
% to faulty components in the removal scenario.

% Actually, the rules above already handle this correctly:
% - Rules with "C2 != C, not faulty(C2)" apply to non-C, non-faulty components
% - Rules with "C" apply to C itself (which is working)
% - For faulty components other than C, alt_val is free (from the choice rule)

% Wait, the issue is that a faulty component C2 (C2 != C) should NOT have its output
% determined by the gate logic. Let me re-examine.

% The rules for working components only fire when the component is NOT faulty:
% "C2 != C, not faulty(C2)" means C2 is not C AND not faulty.
% So faulty components are correctly excluded from the working rules.

% And for C: the "C itself working" rules apply to C.
% So C is forced to be working.

% Faulty components other than C: their alt_val is free (from the choice rule).
% This is correct!

% Now, the removal scenario for C is satisfiable if observations match
removal_possible(C) :- component(C), 
    alt_val(C, out1, 1), alt_val(C, out2, 0).

% If removal is possible for any faulty component, the diagnosis is not minimal
:- faulty(C), removal_possible(C).

% ----- Output -----
% Output the diagnosis (set of faulty components)
% We need to show which components are faulty

% Sort components alphabetically for consistent output
comp_order(and1, 1). comp_order(and2, 2). comp_order(notgate1, 3). comp_order(or1, 4). comp_order(xor1, 5).

% Define diagnosis as the set of faulty components
#show faulty/1.
#show diagnosis/0.