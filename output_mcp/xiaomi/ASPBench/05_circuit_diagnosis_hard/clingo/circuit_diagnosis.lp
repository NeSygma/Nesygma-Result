% Circuit Fault Diagnosis Problem
% Find minimum-cost set of at most 3 faults explaining all 8 test cases

% ============ DOMAIN DEFINITIONS ============

% Test cases
test(1..8).

% Wire names (primary inputs, intermediate wires, primary outputs)
wire(in1). wire(in2). wire(in3). wire(in4). wire(in5).
wire(in6). wire(in7). wire(in8). wire(in9). wire(in10).
wire(w1). wire(w2). wire(w3). wire(w4). wire(w5).
wire(w6). wire(w7). wire(w8). wire(w9). wire(w10).
wire(w11). wire(w12). wire(w13). wire(w14). wire(w15).
wire(w16). wire(w17). wire(w18). wire(w19). wire(w20).
wire(w21). wire(w22). wire(w23). wire(w24). wire(w25).
wire(w26). wire(w27). wire(w28). wire(w29). wire(w30).
wire(w31). wire(w32). wire(u1). wire(u2). wire(u3).
wire(out1). wire(out2). wire(out3).

% Primary inputs
primary_input(in1). primary_input(in2). primary_input(in3). primary_input(in4).
primary_input(in5). primary_input(in6). primary_input(in7). primary_input(in8).
primary_input(in9). primary_input(in10).

% Primary outputs
primary_output(out1). primary_output(out2). primary_output(out3).

% Gate definitions: gate(GateName, Type, Input1, Input2, Output)
% For NOT gates, Input2 is unused (use 'none')

% Layer 1
gate(and1, and, in1, in2, w1).
gate(xor1, xor, in3, in4, w2).
gate(or1, or, in5, in6, w3).
gate(and2, and, in7, in8, w4).
gate(xor2, xor, in9, in10, w5).
gate(not1, not, in1, none, w6).
gate(or2, or, in3, in5, w7).
gate(and3, and, in4, in6, w8).

% Layer 2
gate(and4, and, w1, w2, w9).
gate(or3, or, w3, w4, w10).
gate(xor4, xor, w5, w6, w11).
gate(and5, and, w2, w7, w12).
gate(or4, or, w8, w5, w13).
gate(not2, not, w7, none, w14).
gate(xor5, xor, w6, w1, w15).
gate(and6, and, w4, w8, w16).

% Layer 3
gate(xor6, xor, w9, w10, w17).
gate(and7, and, w11, w12, w18).
gate(or5, or, w13, w14, w19).
gate(xor7, xor, w15, w16, w20).
gate(and8, and, w9, w13, w21).
gate(or6, or, w10, w12, w22).
gate(not3, not, w11, none, w23).
gate(xor8, xor, w14, w16, w24).

% Layer 4
gate(and9, and, w17, w18, w25).
gate(or7, or, w19, w20, w26).
gate(xor9, xor, w21, w22, w27).
gate(and10, and, w23, w24, w28).
gate(or8, or, w25, w26, w29).
gate(xor10, xor, w27, w28, w30).
gate(and11, and, w22, w24, w31).
gate(or9, or, w21, w23, w32).

% Final Stage
gate(xor11, xor, w29, w30, u1).
gate(and12, and, w31, w32, u2).
gate(or10, or, w17, w29, u3).
gate(not4, not, u2, none, out2).
gate(or11, or, u1, u3, out1).
gate(xor12, xor, w30, w31, out3).

% Gate names
gate_name(and1). gate_name(xor1). gate_name(or1). gate_name(and2).
gate_name(xor2). gate_name(not1). gate_name(or2). gate_name(and3).
gate_name(and4). gate_name(or3). gate_name(xor4). gate_name(and5).
gate_name(or4). gate_name(not2). gate_name(xor5). gate_name(and6).
gate_name(xor6). gate_name(and7). gate_name(or5). gate_name(xor7).
gate_name(and8). gate_name(or6). gate_name(not3). gate_name(xor8).
gate_name(and9). gate_name(or7). gate_name(xor9). gate_name(and10).
gate_name(or8). gate_name(xor10). gate_name(and11). gate_name(or9).
gate_name(xor11). gate_name(and12). gate_name(or10). gate_name(not4).
gate_name(or11). gate_name(xor12).

% Fault modes
fault_mode(stuck0). fault_mode(stuck1). fault_mode(invert). fault_mode(open).

% Fault costs
fault_cost(stuck0, 1).
fault_cost(stuck1, 1).
fault_cost(invert, 1).
fault_cost(open, 2).

% ============ TEST CASE INPUTS ============

% Test 1
input_val(1, in1, 1). input_val(1, in2, 1). input_val(1, in3, 0). input_val(1, in4, 1).
input_val(1, in5, 1). input_val(1, in6, 0). input_val(1, in7, 1). input_val(1, in8, 0).
input_val(1, in9, 1). input_val(1, in10, 0).

% Test 2
input_val(2, in1, 0). input_val(2, in2, 1). input_val(2, in3, 1). input_val(2, in4, 0).
input_val(2, in5, 1). input_val(2, in6, 1). input_val(2, in7, 0). input_val(2, in8, 1).
input_val(2, in9, 1). input_val(2, in10, 1).

% Test 3
input_val(3, in1, 1). input_val(3, in2, 0). input_val(3, in3, 1). input_val(3, in4, 1).
input_val(3, in5, 0). input_val(3, in6, 0). input_val(3, in7, 1). input_val(3, in8, 1).
input_val(3, in9, 0). input_val(3, in10, 0).

% Test 4
input_val(4, in1, 0). input_val(4, in2, 0). input_val(4, in3, 0). input_val(4, in4, 1).
input_val(4, in5, 1). input_val(4, in6, 1). input_val(4, in7, 1). input_val(4, in8, 0).
input_val(4, in9, 0). input_val(4, in10, 1).

% Test 5
input_val(5, in1, 1). input_val(5, in2, 1). input_val(5, in3, 1). input_val(5, in4, 1).
input_val(5, in5, 0). input_val(5, in6, 1). input_val(5, in7, 0). input_val(5, in8, 0).
input_val(5, in9, 1). input_val(5, in10, 0).

% Test 6
input_val(6, in1, 0). input_val(6, in2, 1). input_val(6, in3, 0). input_val(6, in4, 0).
input_val(6, in5, 1). input_val(6, in6, 0). input_val(6, in7, 1). input_val(6, in8, 1).
input_val(6, in9, 0). input_val(6, in10, 1).

% Test 7
input_val(7, in1, 1). input_val(7, in2, 0). input_val(7, in3, 0). input_val(7, in4, 1).
input_val(7, in5, 0). input_val(7, in6, 1). input_val(7, in7, 1). input_val(7, in8, 0).
input_val(7, in9, 1). input_val(7, in10, 1).

% Test 8
input_val(8, in1, 0). input_val(8, in2, 0). input_val(8, in3, 1). input_val(8, in4, 0).
input_val(8, in5, 1). input_val(8, in6, 0). input_val(8, in7, 0). input_val(8, in8, 1).
input_val(8, in9, 1). input_val(8, in10, 0).

% ============ OBSERVED OUTPUTS ============

% All tests observe (0, 1, 0)
observed(T, out1, 0) :- test(T).
observed(T, out2, 1) :- test(T).
observed(T, out3, 0) :- test(T).

% ============ FAULT SELECTION ============

% Each gate can have at most one fault mode (or no fault)
{ fault(G, F) : fault_mode(F) } 1 :- gate_name(G).

% At most 3 gates can be faulty
:- #count { G : gate_name(G), fault(G, _) } > 3.

% A gate is faulty if it has a fault assignment
is_faulty(G) :- fault(G, _).

% ============ WIRE VALUE COMPUTATION ============

% Primary input values are fixed per test
val(T, W, V) :- input_val(T, W, V), test(T), primary_input(W).

% Normal gate computation (when gate is not faulty)
% AND gate: output = input1 AND input2
val(T, Out, 1) :- gate(G, and, In1, In2, Out), test(T), 
                   val(T, In1, 1), val(T, In2, 1), is_not_faulty(G).
val(T, Out, 0) :- gate(G, and, In1, In2, Out), test(T),
                   val(T, In1, 0), is_not_faulty(G).
val(T, Out, 0) :- gate(G, and, In1, In2, Out), test(T),
                   val(T, In2, 0), is_not_faulty(G).

% OR gate: output = input1 OR input2
val(T, Out, 1) :- gate(G, or, In1, In2, Out), test(T),
                   val(T, In1, 1), is_not_faulty(G).
val(T, Out, 1) :- gate(G, or, In1, In2, Out), test(T),
                   val(T, In2, 1), is_not_faulty(G).
val(T, Out, 0) :- gate(G, or, In1, In2, Out), test(T),
                   val(T, In1, 0), val(T, In2, 0), is_not_faulty(G).

% XOR gate: output = input1 XOR input2
val(T, Out, 1) :- gate(G, xor, In1, In2, Out), test(T),
                   val(T, In1, 0), val(T, In2, 1), is_not_faulty(G).
val(T, Out, 1) :- gate(G, xor, In1, In2, Out), test(T),
                   val(T, In1, 1), val(T, In2, 0), is_not_faulty(G).
val(T, Out, 0) :- gate(G, xor, In1, In2, Out), test(T),
                   val(T, In1, 0), val(T, In2, 0), is_not_faulty(G).
val(T, Out, 0) :- gate(G, xor, In1, In2, Out), test(T),
                   val(T, In1, 1), val(T, In2, 1), is_not_faulty(G).

% NOT gate: output = NOT input1
val(T, Out, 0) :- gate(G, not, In1, _, Out), test(T),
                   val(T, In1, 1), is_not_faulty(G).
val(T, Out, 1) :- gate(G, not, In1, _, Out), test(T),
                   val(T, In1, 0), is_not_faulty(G).

% Helper: gate is not faulty
is_not_faulty(G) :- gate_name(G), not is_faulty(G).

% ============ FAULTY GATE BEHAVIOR ============

% stuck0: output is always 0
val(T, Out, 0) :- gate(G, _, _, _, Out), test(T), fault(G, stuck0).

% stuck1: output is always 1
val(T, Out, 1) :- gate(G, _, _, _, Out), test(T), fault(G, stuck1).

% invert: output is flipped from correct value
% For invert, we compute what the normal output would be, then negate
val(T, Out, 0) :- gate(G, and, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 1), val(T, In2, 1).
val(T, Out, 1) :- gate(G, and, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 0).
val(T, Out, 1) :- gate(G, and, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In2, 0).
val(T, Out, 0) :- gate(G, or, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 1).
val(T, Out, 0) :- gate(G, or, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In2, 1).
val(T, Out, 1) :- gate(G, or, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 0), val(T, In2, 0).
val(T, Out, 0) :- gate(G, xor, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 0), val(T, In2, 1).
val(T, Out, 0) :- gate(G, xor, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 1), val(T, In2, 0).
val(T, Out, 1) :- gate(G, xor, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 0), val(T, In2, 0).
val(T, Out, 1) :- gate(G, xor, In1, In2, Out), test(T), fault(G, invert),
                   val(T, In1, 1), val(T, In2, 1).
val(T, Out, 1) :- gate(G, not, In1, _, Out), test(T), fault(G, invert),
                   val(T, In1, 1).
val(T, Out, 0) :- gate(G, not, In1, _, Out), test(T), fault(G, invert),
                   val(T, In1, 0).

% open: output can be arbitrary (0 or 1) per test
{ val(T, Out, 0) } :- gate(G, _, _, _, Out), test(T), fault(G, open).
{ val(T, Out, 1) } :- gate(G, _, _, _, Out), test(T), fault(G, open).

% ============ CONSTRAINTS ============

% Each wire must have exactly one value per test
1 { val(T, W, 0); val(T, W, 1) } 1 :- test(T), wire(W).

% Observed outputs must match
:- test(T), primary_output(W), observed(T, W, V), not val(T, W, V).

% ============ COST COMPUTATION ============

% Total cost
total_cost(C) :- C = #sum { Cost, G : fault(G, F), fault_cost(F, Cost) }.

% ============ OPTIMIZATION ============

#minimize { C : total_cost(C) }.

% ============ OUTPUT ============

#show fault/2.
#show total_cost/1.