% Circuit Fault Diagnosis Problem
% Find minimum-cost diagnosis explaining why all 8 test cases produce (0,1,0)

% ===== TEST CASES =====
test(1..8).

% Test 1 inputs
in_val(1, in1, 1). in_val(1, in2, 1). in_val(1, in3, 0). in_val(1, in4, 1).
in_val(1, in5, 1). in_val(1, in6, 0). in_val(1, in7, 1). in_val(1, in8, 0).
in_val(1, in9, 1). in_val(1, in10, 0).

% Test 2 inputs
in_val(2, in1, 0). in_val(2, in2, 1). in_val(2, in3, 1). in_val(2, in4, 0).
in_val(2, in5, 1). in_val(2, in6, 1). in_val(2, in7, 0). in_val(2, in8, 1).
in_val(2, in9, 1). in_val(2, in10, 1).

% Test 3 inputs
in_val(3, in1, 1). in_val(3, in2, 0). in_val(3, in3, 1). in_val(3, in4, 1).
in_val(3, in5, 0). in_val(3, in6, 0). in_val(3, in7, 1). in_val(3, in8, 1).
in_val(3, in9, 0). in_val(3, in10, 0).

% Test 4 inputs
in_val(4, in1, 0). in_val(4, in2, 0). in_val(4, in3, 0). in_val(4, in4, 1).
in_val(4, in5, 1). in_val(4, in6, 1). in_val(4, in7, 1). in_val(4, in8, 0).
in_val(4, in9, 0). in_val(4, in10, 1).

% Test 5 inputs
in_val(5, in1, 1). in_val(5, in2, 1). in_val(5, in3, 1). in_val(5, in4, 1).
in_val(5, in5, 0). in_val(5, in6, 1). in_val(5, in7, 0). in_val(5, in8, 0).
in_val(5, in9, 1). in_val(5, in10, 0).

% Test 6 inputs
in_val(6, in1, 0). in_val(6, in2, 1). in_val(6, in3, 0). in_val(6, in4, 0).
in_val(6, in5, 1). in_val(6, in6, 0). in_val(6, in7, 1). in_val(6, in8, 1).
in_val(6, in9, 0). in_val(6, in10, 1).

% Test 7 inputs
in_val(7, in1, 1). in_val(7, in2, 0). in_val(7, in3, 0). in_val(7, in4, 1).
in_val(7, in5, 0). in_val(7, in6, 1). in_val(7, in7, 1). in_val(7, in8, 0).
in_val(7, in9, 1). in_val(7, in10, 1).

% Test 8 inputs
in_val(8, in1, 0). in_val(8, in2, 0). in_val(8, in3, 1). in_val(8, in4, 0).
in_val(8, in5, 1). in_val(8, in6, 0). in_val(8, in7, 0). in_val(8, in8, 1).
in_val(8, in9, 1). in_val(8, in10, 0).

% Observed outputs for all tests: (0,1,0)
observed(T, out1, 0) :- test(T).
observed(T, out2, 1) :- test(T).
observed(T, out3, 0) :- test(T).

% ===== CIRCUIT STRUCTURE =====
% Gate definitions: gate(GateName, GateType)
% Gate inputs: gate_in(GateName, InputWire, Position)
% Gate output: gate_out(GateName, OutputWire)

% Layer 1 gates
gate(and1, and). gate_in(and1, in1, 1). gate_in(and1, in2, 2). gate_out(and1, w1).
gate(xor1, xor). gate_in(xor1, in3, 1). gate_in(xor1, in4, 2). gate_out(xor1, w2).
gate(or1, or). gate_in(or1, in5, 1). gate_in(or1, in6, 2). gate_out(or1, w3).
gate(and2, and). gate_in(and2, in7, 1). gate_in(and2, in8, 2). gate_out(and2, w4).
gate(xor2, xor). gate_in(xor2, in9, 1). gate_in(xor2, in10, 2). gate_out(xor2, w5).
gate(not1, neg). gate_in(not1, in1, 1). gate_out(not1, w6).
gate(or2, or). gate_in(or2, in3, 1). gate_in(or2, in5, 2). gate_out(or2, w7).
gate(and3, and). gate_in(and3, in4, 1). gate_in(and3, in6, 2). gate_out(and3, w8).

% Layer 2 gates
gate(and4, and). gate_in(and4, w1, 1). gate_in(and4, w2, 2). gate_out(and4, w9).
gate(or3, or). gate_in(or3, w3, 1). gate_in(or3, w4, 2). gate_out(or3, w10).
gate(xor4, xor). gate_in(xor4, w5, 1). gate_in(xor4, w6, 2). gate_out(xor4, w11).
gate(and5, and). gate_in(and5, w2, 1). gate_in(and5, w7, 2). gate_out(and5, w12).
gate(or4, or). gate_in(or4, w8, 1). gate_in(or4, w5, 2). gate_out(or4, w13).
gate(not2, neg). gate_in(not2, w7, 1). gate_out(not2, w14).
gate(xor5, xor). gate_in(xor5, w6, 1). gate_in(xor5, w1, 2). gate_out(xor5, w15).
gate(and6, and). gate_in(and6, w4, 1). gate_in(and6, w8, 2). gate_out(and6, w16).

% Layer 3 gates
gate(xor6, xor). gate_in(xor6, w9, 1). gate_in(xor6, w10, 2). gate_out(xor6, w17).
gate(and7, and). gate_in(and7, w11, 1). gate_in(and7, w12, 2). gate_out(and7, w18).
gate(or5, or). gate_in(or5, w13, 1). gate_in(or5, w14, 2). gate_out(or5, w19).
gate(xor7, xor). gate_in(xor7, w15, 1). gate_in(xor7, w16, 2). gate_out(xor7, w20).
gate(and8, and). gate_in(and8, w9, 1). gate_in(and8, w13, 2). gate_out(and8, w21).
gate(or6, or). gate_in(or6, w10, 1). gate_in(or6, w12, 2). gate_out(or6, w22).
gate(not3, neg). gate_in(not3, w11, 1). gate_out(not3, w23).
gate(xor8, xor). gate_in(xor8, w14, 1). gate_in(xor8, w16, 2). gate_out(xor8, w24).

% Layer 4 gates
gate(and9, and). gate_in(and9, w17, 1). gate_in(and9, w18, 2). gate_out(and9, w25).
gate(or7, or). gate_in(or7, w19, 1). gate_in(or7, w20, 2). gate_out(or7, w26).
gate(xor9, xor). gate_in(xor9, w21, 1). gate_in(xor9, w22, 2). gate_out(xor9, w27).
gate(and10, and). gate_in(and10, w23, 1). gate_in(and10, w24, 2). gate_out(and10, w28).
gate(or8, or). gate_in(or8, w25, 1). gate_in(or8, w26, 2). gate_out(or8, w29).
gate(xor10, xor). gate_in(xor10, w27, 1). gate_in(xor10, w28, 2). gate_out(xor10, w30).
gate(and11, and). gate_in(and11, w22, 1). gate_in(and11, w24, 2). gate_out(and11, w31).
gate(or9, or). gate_in(or9, w21, 1). gate_in(or9, w23, 2). gate_out(or9, w32).

% Final stage gates
gate(xor11, xor). gate_in(xor11, w29, 1). gate_in(xor11, w30, 2). gate_out(xor11, u1).
gate(and12, and). gate_in(and12, w31, 1). gate_in(and12, w32, 2). gate_out(and12, u2).
gate(or10, or). gate_in(or10, w17, 1). gate_in(or10, w29, 2). gate_out(or10, u3).
gate(not4, neg). gate_in(not4, u2, 1). gate_out(not4, out2).
gate(or11, or). gate_in(or11, u1, 1). gate_in(or11, u3, 2). gate_out(or11, out1).
gate(xor12, xor). gate_in(xor12, w30, 1). gate_in(xor12, w31, 2). gate_out(xor12, out3).

% ===== FAULT MODES AND COSTS =====
fault_mode(none). fault_mode(stuck0). fault_mode(stuck1). fault_mode(invert). fault_mode(open).
cost(none, 0). cost(stuck0, 1). cost(stuck1, 1). cost(invert, 1). cost(open, 2).

% ===== CHOICE RULES =====
% Each gate can have exactly one fault mode (including none)
{ fault(G, Mode) : fault_mode(Mode) } = 1 :- gate(G, _).

% ===== WIRE VALUES =====
% Primary inputs are given by test cases
wire_val(T, Input, Value) :- in_val(T, Input, Value).

% Compute normal gate output (without faults)
% AND gate: output 1 only if both inputs are 1
normal_output(T, G, 1) :- gate(G, and), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 1), wire_val(T, I2, 1).
normal_output(T, G, 0) :- gate(G, and), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 0), wire_val(T, I2, 0).
normal_output(T, G, 0) :- gate(G, and), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 0), wire_val(T, I2, 1).
normal_output(T, G, 0) :- gate(G, and), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 1), wire_val(T, I2, 0).

% OR gate: output 1 if at least one input is 1
normal_output(T, G, 0) :- gate(G, or), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 0), wire_val(T, I2, 0).
normal_output(T, G, 1) :- gate(G, or), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 0), wire_val(T, I2, 1).
normal_output(T, G, 1) :- gate(G, or), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 1), wire_val(T, I2, 0).
normal_output(T, G, 1) :- gate(G, or), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 1), wire_val(T, I2, 1).

% XOR gate: output 1 if inputs are different
normal_output(T, G, 0) :- gate(G, xor), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 0), wire_val(T, I2, 0).
normal_output(T, G, 1) :- gate(G, xor), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 0), wire_val(T, I2, 1).
normal_output(T, G, 1) :- gate(G, xor), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 1), wire_val(T, I2, 0).
normal_output(T, G, 0) :- gate(G, xor), gate_in(G, I1, 1), gate_in(G, I2, 2), 
                          wire_val(T, I1, 1), wire_val(T, I2, 1).

% NOT gate: invert input
normal_output(T, G, 0) :- gate(G, neg), gate_in(G, I1, 1), wire_val(T, I1, 1).
normal_output(T, G, 1) :- gate(G, neg), gate_in(G, I1, 1), wire_val(T, I1, 0).

% ===== GATE OUTPUTS WITH FAULTS =====
% No fault: output equals normal output
wire_val(T, Output, Normal) :- fault(G, none), normal_output(T, G, Normal), 
                               gate_out(G, Output), test(T).

% Stuck-at-0: output always 0
wire_val(T, Output, 0) :- fault(G, stuck0), gate_out(G, Output), test(T).

% Stuck-at-1: output always 1
wire_val(T, Output, 1) :- fault(G, stuck1), gate_out(G, Output), test(T).

% Invert: output is flipped normal output
wire_val(T, Output, 1) :- fault(G, invert), normal_output(T, G, 0), 
                          gate_out(G, Output), test(T).
wire_val(T, Output, 0) :- fault(G, invert), normal_output(T, G, 1), 
                          gate_out(G, Output), test(T).

% Open: output can be 0 or 1 (choice per test)
{ wire_val(T, Output, 0); wire_val(T, Output, 1) } = 1 :- fault(G, open), 
                                                          gate_out(G, Output), test(T).

% ===== CONSTRAINTS =====
% Observed outputs must match computed values
:- test(T), observed(T, Output, Value), not wire_val(T, Output, Value).

% At most 3 gates can be faulty
:- #count{ G : fault(G, Mode), Mode != none } > 3.

% ===== OPTIMIZATION =====
% Minimize total fault cost
#minimize { Cost, G, Mode : fault(G, Mode), cost(Mode, Cost) }.

% ===== OUTPUT =====
% Show only faulty gates (not none)
#show fault(G, Mode) : fault(G, Mode), Mode != none.

% Show total cost
total_cost(Cost) :- Cost = #sum{ C, G, Mode : fault(G, Mode), cost(Mode, C) }.
#show total_cost/1.