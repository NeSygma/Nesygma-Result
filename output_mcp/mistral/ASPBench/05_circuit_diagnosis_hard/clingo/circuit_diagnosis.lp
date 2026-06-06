% Circuit Diagnosis Problem
% =========================

% Domain declarations

% Gates (46 total)
gate(and1; and2; and3; and4; and5; and6; and7; and8; and9; and10; and11; and12).
gate(xor1; xor2; xor4; xor5; xor6; xor7; xor8; xor9; xor10; xor11; xor12).
gate(or1; or2; or3; or4; or5; or6; or7; or8; or9; or10; or11).
gate(not1; not2; not3; not4).

% Gate types
and_gate(G) :- gate(G), G = and1..and12.
xor_gate(G) :- gate(G), G = xor1..xor12.
or_gate(G) :- gate(G), G = or1..or11.
not_gate(G) :- gate(G), G = not1..not4.

% Primary inputs
input(in1; in2; in3; in4; in5; in6; in7; in8; in9; in10).

% Primary outputs
output(out1; out2; out3).

% Wires
wire(w1; w2; w3; w4; w5; w6; w7; w8; w9; w10; w11; w12; w13; w14; w15; w16; w17; w18; w19; w20; w21; w22; w23; w24; w25; w26; w27; w28; w29; w30; w31; w32).
wire(u1; u2; u3).

% Test cases
test(1..8).

% Circuit structure (inputs to gates)
% Layer 1
input_wire(and1, in1).
input_wire(and1, in2).
input_wire(xor1, in3).
input_wire(xor1, in4).
input_wire(or1, in5).
input_wire(or1, in6).
input_wire(and2, in7).
input_wire(and2, in8).
input_wire(xor2, in9).
input_wire(xor2, in10).
input_wire(not1, in1).
input_wire(or2, in3).
input_wire(or2, in5).
input_wire(and3, in4).
input_wire(and3, in6).

% Layer 2
input_wire(and4, w1).
input_wire(and4, w2).
input_wire(or3, w3).
input_wire(or3, w4).
input_wire(xor4, w5).
input_wire(xor4, w6).
input_wire(and5, w2).
input_wire(and5, w7).
input_wire(or4, w8).
input_wire(or4, w5).
input_wire(not2, w7).
input_wire(xor5, w6).
input_wire(xor5, w1).
input_wire(and6, w4).
input_wire(and6, w8).

% Layer 3
input_wire(xor6, w9).
input_wire(xor6, w10).
input_wire(and7, w11).
input_wire(and7, w12).
input_wire(or5, w13).
input_wire(or5, w14).
input_wire(xor7, w15).
input_wire(xor7, w16).
input_wire(and8, w9).
input_wire(and8, w13).
input_wire(or6, w10).
input_wire(or6, w12).
input_wire(not3, w11).
input_wire(xor8, w14).
input_wire(xor8, w16).

% Layer 4
input_wire(and9, w17).
input_wire(and9, w18).
input_wire(or7, w19).
input_wire(or7, w20).
input_wire(xor9, w21).
input_wire(xor9, w22).
input_wire(and10, w23).
input_wire(and10, w24).
input_wire(or8, w25).
input_wire(or8, w26).
input_wire(xor10, w27).
input_wire(xor10, w28).
input_wire(and11, w22).
input_wire(and11, w24).
input_wire(or9, w21).
input_wire(or9, w23).

% Final Stage
input_wire(xor11, w29).
input_wire(xor11, w30).
input_wire(and12, w31).
input_wire(and12, w32).
input_wire(or10, w17).
input_wire(or10, w29).
input_wire(not4, u2).
input_wire(or11, u1).
input_wire(or11, u3).
input_wire(xor12, w30).
input_wire(xor12, w31).

% Gate outputs to wires
output_wire(and1, w1).
output_wire(xor1, w2).
output_wire(or1, w3).
output_wire(and2, w4).
output_wire(xor2, w5).
output_wire(not1, w6).
output_wire(or2, w7).
output_wire(and3, w8).
output_wire(and4, w9).
output_wire(or3, w10).
output_wire(xor4, w11).
output_wire(and5, w12).
output_wire(or4, w13).
output_wire(not2, w14).
output_wire(xor5, w15).
output_wire(and6, w16).
output_wire(xor6, w17).
output_wire(and7, w18).
output_wire(or5, w19).
output_wire(xor7, w20).
output_wire(and8, w21).
output_wire(or6, w22).
output_wire(not3, w23).
output_wire(xor8, w24).
output_wire(and9, w25).
output_wire(or7, w26).
output_wire(xor9, w27).
output_wire(and10, w28).
output_wire(or8, w29).
output_wire(xor10, w30).
output_wire(and11, w31).
output_wire(or9, w32).
output_wire(xor11, u1).
output_wire(and12, u2).
output_wire(or10, u3).
output_wire(not4, out2).
output_wire(or11, out1).
output_wire(xor12, out3).

% Test case inputs
% Test 1: in1=1, in2=1, in3=0, in4=1, in5=1, in6=0, in7=1, in8=0, in9=1, in10=0
test_input(1, in1, 1).
test_input(1, in2, 1).
test_input(1, in3, 0).
test_input(1, in4, 1).
test_input(1, in5, 1).
test_input(1, in6, 0).
test_input(1, in7, 1).
test_input(1, in8, 0).
test_input(1, in9, 1).
test_input(1, in10, 0).

% Test 2: in1=0, in2=1, in3=1, in4=0, in5=1, in6=1, in7=0, in8=1, in9=1, in10=1
test_input(2, in1, 0).
test_input(2, in2, 1).
test_input(2, in3, 1).
test_input(2, in4, 0).
test_input(2, in5, 1).
test_input(2, in6, 1).
test_input(2, in7, 0).
test_input(2, in8, 1).
test_input(2, in9, 1).
test_input(2, in10, 1).

% Test 3: in1=1, in2=0, in3=1, in4=1, in5=0, in6=0, in7=1, in8=1, in9=0, in10=0
test_input(3, in1, 1).
test_input(3, in2, 0).
test_input(3, in3, 1).
test_input(3, in4, 1).
test_input(3, in5, 0).
test_input(3, in6, 0).
test_input(3, in7, 1).
test_input(3, in8, 1).
test_input(3, in9, 0).
test_input(3, in10, 0).

% Test 4: in1=0, in2=0, in3=0, in4=1, in5=1, in6=1, in7=1, in8=0, in9=0, in10=1
test_input(4, in1, 0).
test_input(4, in2, 0).
test_input(4, in3, 0).
test_input(4, in4, 1).
test_input(4, in5, 1).
test_input(4, in6, 1).
test_input(4, in7, 1).
test_input(4, in8, 0).
test_input(4, in9, 0).
test_input(4, in10, 1).

% Test 5: in1=1, in2=1, in3=1, in4=1, in5=0, in6=1, in7=0, in8=0, in9=1, in10=0
test_input(5, in1, 1).
test_input(5, in2, 1).
test_input(5, in3, 1).
test_input(5, in4, 1).
test_input(5, in5, 0).
test_input(5, in6, 1).
test_input(5, in7, 0).
test_input(5, in8, 0).
test_input(5, in9, 1).
test_input(5, in10, 0).

% Test 6: in1=0, in2=1, in3=0, in4=0, in5=1, in6=0, in7=1, in8=1, in9=0, in10=1
test_input(6, in1, 0).
test_input(6, in2, 1).
test_input(6, in3, 0).
test_input(6, in4, 0).
test_input(6, in5, 1).
test_input(6, in6, 0).
test_input(6, in7, 1).
test_input(6, in8, 1).
test_input(6, in9, 0).
test_input(6, in10, 1).

% Test 7: in1=1, in2=0, in3=0, in4=1, in5=0, in6=1, in7=1, in8=0, in9=1, in10=1
test_input(7, in1, 1).
test_input(7, in2, 0).
test_input(7, in3, 0).
test_input(7, in4, 1).
test_input(7, in5, 0).
test_input(7, in6, 1).
test_input(7, in7, 1).
test_input(7, in8, 0).
test_input(7, in9, 1).
test_input(7, in10, 1).

% Test 8: in1=0, in2=0, in3=1, in4=0, in5=1, in6=0, in7=0, in8=1, in9=1, in10=0
test_input(8, in1, 0).
test_input(8, in2, 0).
test_input(8, in3, 1).
test_input(8, in4, 0).
test_input(8, in5, 1).
test_input(8, in6, 0).
test_input(8, in7, 0).
test_input(8, in8, 1).
test_input(8, in9, 1).
test_input(8, in10, 0).

% Test case outputs (all tests produce (0,1,0))
test_output(T, out1, 0) :- test(T).
test_output(T, out2, 1) :- test(T).
test_output(T, out3, 0) :- test(T).

% Fault modes and costs
fault_mode(stuck0).
fault_mode(stuck1).
fault_mode(invert).
fault_mode(open).

fault_cost(stuck0, 1).
fault_cost(stuck1, 1).
fault_cost(invert, 1).
fault_cost(open, 2).

% At most 3 gates can be faulty
1 { faulty(G, F) : fault_mode(F) } 1 :- gate(G).
:- { faulty(G, F) : gate(G), fault_mode(F) } 4.

% Signal propagation through the circuit
% Base case: primary inputs have values from test cases
signal(W, T, V) :- test_input(T, I, V), input_wire(G, I), output_wire(G, W).

% For primary inputs that are not connected to any gate input (shouldn't happen, but just in case)
signal(I, T, V) :- test_input(T, I, V), input(I), not wire(I).

% Gate behavior: compute output based on inputs
% AND gate
gate_output(G, T, 1) :- and_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I1, T, 1), signal(I2, T, 1),
    output_wire(G, W).
gate_output(G, T, 0) :- and_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I1, T, 0).
gate_output(G, T, 0) :- and_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I2, T, 0),
    output_wire(G, W).

% OR gate
gate_output(G, T, 1) :- or_gate(G), test(T), 
    input_wire(G, I1), signal(I1, T, 1).
gate_output(G, T, 1) :- or_gate(G), test(T), 
    input_wire(G, I2), signal(I2, T, 1),
    output_wire(G, W).
gate_output(G, T, 0) :- or_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I1, T, 0), signal(I2, T, 0),
    output_wire(G, W).

% XOR gate
gate_output(G, T, 1) :- xor_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I1, T, 0), signal(I2, T, 1),
    output_wire(G, W).
gate_output(G, T, 1) :- xor_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I1, T, 1), signal(I2, T, 0),
    output_wire(G, W).
gate_output(G, T, 0) :- xor_gate(G), test(T), 
    input_wire(G, I1), input_wire(G, I2),
    signal(I1, T, V1), signal(I2, T, V2), V1 == V2,
    output_wire(G, W).

% NOT gate
gate_output(G, T, 1) :- not_gate(G), test(T), 
    input_wire(G, I), signal(I, T, 0),
    output_wire(G, W).
gate_output(G, T, 0) :- not_gate(G), test(T), 
    input_wire(G, I), signal(I, T, 1),
    output_wire(G, W).

% Signal on wires from gate outputs
signal(W, T, V) :- gate_output(G, T, V), output_wire(G, W).

% Faulty behavior overrides correct behavior
% stuck0: output is always 0
signal(W, T, 0) :- faulty(G, stuck0), output_wire(G, W), test(T).

% stuck1: output is always 1
signal(W, T, 1) :- faulty(G, stuck1), output_wire(G, W), test(T).

% invert: output is flipped
signal(W, T, 1) :- faulty(G, invert), output_wire(G, W), gate_output(G, T, 0), test(T).
signal(W, T, 0) :- faulty(G, invert), output_wire(G, W), gate_output(G, T, 1), test(T).

% open: output can be arbitrary (we allow both 0 and 1, no constraint)
% This is implicitly handled by not constraining the signal value

% The diagnosis must explain all test outputs
:- test(T), output(O), test_output(T, O, V),
   signal(O, T, V_other), V != V_other.

% Calculate total cost
total_cost(C) :- C = #sum { Cost : faulty(G, F), fault_cost(F, Cost) }.

% Minimize the total cost
#minimize { Cost : faulty(G, F), fault_cost(F, Cost) }.

% Show the diagnosis
#show faulty/2.
#show total_cost/1.