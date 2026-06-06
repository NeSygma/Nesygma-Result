% Circuit Diagnosis Problem
% 46 logic gates, 8 test cases, find minimal cost diagnosis

% ==================== CIRCUIT STRUCTURE ====================

% Primary inputs
primary_input(in1). primary_input(in2). primary_input(in3). primary_input(in4).
primary_input(in5). primary_input(in6). primary_input(in7). primary_input(in8).
primary_input(in9). primary_input(in10).

% Primary outputs
primary_output(out1). primary_output(out2). primary_output(out3).

% Layer 1 gates (8 gates)
gate(and1, and, in1, in2, w1).
gate(xor1, xor, in3, in4, w2).
gate(or1, or, in5, in6, w3).
gate(and2, and, in7, in8, w4).
gate(xor2, xor, in9, in10, w5).
gate_not(not1, in1, w6).
gate(or2, or, in3, in5, w7).
gate(and3, and, in4, in6, w8).

% Layer 2 gates (8 gates)
gate(and4, and, w1, w2, w9).
gate(or3, or, w3, w4, w10).
gate(xor4, xor, w5, w6, w11).
gate(and5, and, w2, w7, w12).
gate(or4, or, w8, w5, w13).
gate_not(not2, w7, w14).
gate(xor5, xor, w6, w1, w15).
gate(and6, and, w4, w8, w16).

% Layer 3 gates (8 gates)
gate(xor6, xor, w9, w10, w17).
gate(and7, and, w11, w12, w18).
gate(or5, or, w13, w14, w19).
gate(xor7, xor, w15, w16, w20).
gate(and8, and, w9, w13, w21).
gate(or6, or, w10, w12, w22).
gate_not(not3, w11, w23).
gate(xor8, xor, w14, w16, w24).

% Layer 4 gates (8 gates)
gate(and9, and, w17, w18, w25).
gate(or7, or, w19, w20, w26).
gate(xor9, xor, w21, w22, w27).
gate(and10, and, w23, w24, w28).
gate(or8, or, w25, w26, w29).
gate(xor10, xor, w27, w28, w30).
gate(and11, and, w22, w24, w31).
gate(or9, or, w21, w23, w32).

% Final stage gates (6 gates)
gate(xor11, xor, w29, w30, u1).
gate(and12, and, w31, w32, u2).
gate(or10, or, w17, w29, u3).
gate_not(not4, u2, out2).
gate(or11, or, u1, u3, out1).
gate(xor12, xor, w30, w31, out3).

% ==================== TEST CASES ====================
% Test 1
test_input(1, in1, 1). test_input(1, in2, 1). test_input(1, in3, 0).
test_input(1, in4, 1). test_input(1, in5, 1). test_input(1, in6, 0).
test_input(1, in7, 1). test_input(1, in8, 0). test_input(1, in9, 1).
test_input(1, in10, 0).
test_output(1, out1, 0). test_output(1, out2, 1). test_output(1, out3, 0).

% Test 2
test_input(2, in1, 0). test_input(2, in2, 1). test_input(2, in3, 1).
test_input(2, in4, 0). test_input(2, in5, 1). test_input(2, in6, 1).
test_input(2, in7, 0). test_input(2, in8, 1). test_input(2, in9, 1).
test_input(2, in10, 1).
test_output(2, out1, 0). test_output(2, out2, 1). test_output(2, out3, 0).

% Test 3
test_input(3, in1, 1). test_input(3, in2, 0). test_input(3, in3, 1).
test_input(3, in4, 1). test_input(3, in5, 0). test_input(3, in6, 0).
test_input(3, in7, 1). test_input(3, in8, 1). test_input(3, in9, 0).
test_input(3, in10, 0).
test_output(3, out1, 0). test_output(3, out2, 1). test_output(3, out3, 0).

% Test 4
test_input(4, in1, 0). test_input(4, in2, 0). test_input(4, in3, 0).
test_input(4, in4, 1). test_input(4, in5, 1). test_input(4, in6, 1).
test_input(4, in7, 1). test_input(4, in8, 0). test_input(4, in9, 0).
test_input(4, in10, 1).
test_output(4, out1, 0). test_output(4, out2, 1). test_output(4, out3, 0).

% Test 5
test_input(5, in1, 1). test_input(5, in2, 1). test_input(5, in3, 1).
test_input(5, in4, 1). test_input(5, in5, 0). test_input(5, in6, 1).
test_input(5, in7, 0). test_input(5, in8, 0). test_input(5, in9, 1).
test_input(5, in10, 0).
test_output(5, out1, 0). test_output(5, out2, 1). test_output(5, out3, 0).

% Test 6
test_input(6, in1, 0). test_input(6, in2, 1). test_input(6, in3, 0).
test_input(6, in4, 0). test_input(6, in5, 1). test_input(6, in6, 0).
test_input(6, in7, 1). test_input(6, in8, 1). test_input(6, in9, 0).
test_input(6, in10, 1).
test_output(6, out1, 0). test_output(6, out2, 1). test_output(6, out3, 0).

% Test 7
test_input(7, in1, 1). test_input(7, in2, 0). test_input(7, in3, 0).
test_input(7, in4, 1). test_input(7, in5, 0). test_input(7, in6, 1).
test_input(7, in7, 1). test_input(7, in8, 0). test_input(7, in9, 1).
test_input(7, in10, 1).
test_output(7, out1, 0). test_output(7, out2, 1). test_output(7, out3, 0).

% Test 8
test_input(8, in1, 0). test_input(8, in2, 0). test_input(8, in3, 1).
test_input(8, in4, 0). test_input(8, in5, 1). test_input(8, in6, 0).
test_input(8, in7, 0). test_input(8, in8, 1). test_input(8, in9, 1).
test_input(8, in10, 0).
test_output(8, out1, 0). test_output(8, out2, 1). test_output(8, out3, 0).

% ==================== FAULT MODELS ====================
% Fault modes with costs
fault_mode(stuck0, 1).
fault_mode(stuck1, 1).
fault_mode(invert, 1).
fault_mode(open, 2).

% Each gate can have at most one fault mode
{ fault(Gate, Mode) : fault_mode(Mode, _) } 1 :- gate(Gate, _, _, _, _).
{ fault(Gate, Mode) : fault_mode(Mode, _) } 1 :- gate_not(Gate, _, _).

% Faulty gates
faulty(Gate) :- fault(Gate, _).

% ==================== VALUE PROPAGATION ====================
% Correct values (without faults) for each test
% Primary inputs
correct_value(Test, Input, Value) :- test_input(Test, Input, Value).

% Gate outputs (correct computation)
% Two-input gates
correct_value(Test, Output, Val) :-
    gate(Gate, Type, In1, In2, Output),
    correct_value(Test, In1, V1),
    correct_value(Test, In2, V2),
    compute_gate(Type, V1, V2, Val).

% NOT gates
correct_value(Test, Output, Val) :-
    gate_not(Gate, Input, Output),
    correct_value(Test, Input, V),
    Val = 1 - V.

% Gate computation rules
compute_gate(and, 1, 1, 1).
compute_gate(and, 1, 0, 0).
compute_gate(and, 0, 1, 0).
compute_gate(and, 0, 0, 0).
compute_gate(or, 0, 0, 0).
compute_gate(or, 0, 1, 1).
compute_gate(or, 1, 0, 1).
compute_gate(or, 1, 1, 1).
compute_gate(xor, 0, 0, 0).
compute_gate(xor, 0, 1, 1).
compute_gate(xor, 1, 0, 1).
compute_gate(xor, 1, 1, 0).

% Actual values with faults
% For primary inputs (no faults possible)
actual_value(Test, Input, Value) :- primary_input(Input), correct_value(Test, Input, Value).

% For gate outputs with faults
% If gate has stuck0 fault: output is always 0
actual_value(Test, Output, 0) :-
    gate(Gate, _, _, _, Output),
    fault(Gate, stuck0),
    test(Test).

% If gate has stuck1 fault: output is always 1
actual_value(Test, Output, 1) :-
    gate(Gate, _, _, _, Output),
    fault(Gate, stuck1),
    test(Test).

% If gate has invert fault: output is inverted correct value
actual_value(Test, Output, Inv) :-
    gate(Gate, _, _, _, Output),
    fault(Gate, invert),
    correct_value(Test, Output, Val),
    Inv = 1 - Val.

% If gate has open fault: output can be arbitrary per test
% We need to choose a value for each test when gate is open
{ open_value(Test, Gate, 0..1) } :- fault(Gate, open), test(Test).
actual_value(Test, Output, Val) :-
    gate(Gate, _, _, _, Output),
    fault(Gate, open),
    open_value(Test, Gate, Val).

% For gates without faults: use correct value
actual_value(Test, Output, Val) :-
    gate(Gate, _, _, _, Output),
    not faulty(Gate),
    correct_value(Test, Output, Val).

% Same for NOT gates
actual_value(Test, Output, 0) :-
    gate_not(Gate, _, Output),
    fault(Gate, stuck0),
    test(Test).

actual_value(Test, Output, 1) :-
    gate_not(Gate, _, Output),
    fault(Gate, stuck1),
    test(Test).

actual_value(Test, Output, Inv) :-
    gate_not(Gate, _, Output),
    fault(Gate, invert),
    correct_value(Test, Output, Val),
    Inv = 1 - Val.

actual_value(Test, Output, Val) :-
    gate_not(Gate, _, Output),
    fault(Gate, open),
    open_value(Test, Gate, Val).

actual_value(Test, Output, Val) :-
    gate_not(Gate, _, Output),
    not faulty(Gate),
    correct_value(Test, Output, Val).

% ==================== CONSTRAINTS ====================
% Test domain
test(1..8).

% At most 3 faulty gates
:- #count{ Gate : faulty(Gate) } > 3.

% Consistency: actual outputs must match observed outputs for all tests
:- test(Test), primary_output(Output),
   actual_value(Test, Output, Actual),
   test_output(Test, Output, Expected),
   Actual != Expected.

% ==================== OPTIMIZATION ====================
% Total cost
total_cost(Cost) :-
    Cost = #sum{ C, Gate : fault(Gate, Mode), fault_mode(Mode, C) }.

% Minimize total cost
#minimize { C : total_cost(C) }.

% ==================== OUTPUT ====================
% Show the diagnosis
#show fault/2.
#show total_cost/1.
#show faulty/1.

% Also show which gates are faulty with their modes
diagnosis(Gate, Mode, Cost) :- fault(Gate, Mode), fault_mode(Mode, Cost).
#show diagnosis/3.