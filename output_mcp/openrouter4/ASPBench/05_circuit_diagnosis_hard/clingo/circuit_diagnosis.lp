%%% Circuit Diagnosis Problem
%%% Find minimum-cost faults explaining observed outputs

%% ========== DOMAIN ==========
test(1..8).

%% Fault modes
fault_mode(stuck0; stuck1; invert; open).

%% Fault costs
fault_cost(stuck0, 1).
fault_cost(stuck1, 1).
fault_cost(invert, 1).
fault_cost(open, 2).

%% Primary inputs
primary_input(in1; in2; in3; in4; in5; in6; in7; in8; in9; in10).

%% ========== TEST INPUT DATA ==========
%% Test 1: in1=1, in2=1, in3=0, in4=1, in5=1, in6=0, in7=1, in8=0, in9=1, in10=0
input_val(1, in1, 1). input_val(1, in2, 1). input_val(1, in3, 0). input_val(1, in4, 1). input_val(1, in5, 1).
input_val(1, in6, 0). input_val(1, in7, 1). input_val(1, in8, 0). input_val(1, in9, 1). input_val(1, in10, 0).

%% Test 2: in1=0, in2=1, in3=1, in4=0, in5=1, in6=1, in7=0, in8=1, in9=1, in10=1
input_val(2, in1, 0). input_val(2, in2, 1). input_val(2, in3, 1). input_val(2, in4, 0). input_val(2, in5, 1).
input_val(2, in6, 1). input_val(2, in7, 0). input_val(2, in8, 1). input_val(2, in9, 1). input_val(2, in10, 1).

%% Test 3: in1=1, in2=0, in3=1, in4=1, in5=0, in6=0, in7=1, in8=1, in9=0, in10=0
input_val(3, in1, 1). input_val(3, in2, 0). input_val(3, in3, 1). input_val(3, in4, 1). input_val(3, in5, 0).
input_val(3, in6, 0). input_val(3, in7, 1). input_val(3, in8, 1). input_val(3, in9, 0). input_val(3, in10, 0).

%% Test 4: in1=0, in2=0, in3=0, in4=1, in5=1, in6=1, in7=1, in8=0, in9=0, in10=1
input_val(4, in1, 0). input_val(4, in2, 0). input_val(4, in3, 0). input_val(4, in4, 1). input_val(4, in5, 1).
input_val(4, in6, 1). input_val(4, in7, 1). input_val(4, in8, 0). input_val(4, in9, 0). input_val(4, in10, 1).

%% Test 5: in1=1, in2=1, in3=1, in4=1, in5=0, in6=1, in7=0, in8=0, in9=1, in10=0
input_val(5, in1, 1). input_val(5, in2, 1). input_val(5, in3, 1). input_val(5, in4, 1). input_val(5, in5, 0).
input_val(5, in6, 1). input_val(5, in7, 0). input_val(5, in8, 0). input_val(5, in9, 1). input_val(5, in10, 0).

%% Test 6: in1=0, in2=1, in3=0, in4=0, in5=1, in6=0, in7=1, in8=1, in9=0, in10=1
input_val(6, in1, 0). input_val(6, in2, 1). input_val(6, in3, 0). input_val(6, in4, 0). input_val(6, in5, 1).
input_val(6, in6, 0). input_val(6, in7, 1). input_val(6, in8, 1). input_val(6, in9, 0). input_val(6, in10, 1).

%% Test 7: in1=1, in2=0, in3=0, in4=1, in5=0, in6=1, in7=1, in8=0, in9=1, in10=1
input_val(7, in1, 1). input_val(7, in2, 0). input_val(7, in3, 0). input_val(7, in4, 1). input_val(7, in5, 0).
input_val(7, in6, 1). input_val(7, in7, 1). input_val(7, in8, 0). input_val(7, in9, 1). input_val(7, in10, 1).

%% Test 8: in1=0, in2=0, in3=1, in4=0, in5=1, in6=0, in7=0, in8=1, in9=1, in10=0
input_val(8, in1, 0). input_val(8, in2, 0). input_val(8, in3, 1). input_val(8, in4, 0). input_val(8, in5, 1).
input_val(8, in6, 0). input_val(8, in7, 0). input_val(8, in8, 1). input_val(8, in9, 1). input_val(8, in10, 0).

%% ========== CIRCUIT STRUCTURE ==========
%% gate(GateName, Type, Input1, Input2, OutputWire)
%% Types: and, or, xor, neg (for NOT)
%% For neg gates, Input2 is "none"

%% Layer 1
gate(and1, and, in1, in2, w1).
gate(xor1, xor, in3, in4, w2).
gate(or1, or, in5, in6, w3).
gate(and2, and, in7, in8, w4).
gate(xor2, xor, in9, in10, w5).
gate(not1, neg, in1, none, w6).
gate(or2, or, in3, in5, w7).
gate(and3, and, in4, in6, w8).

%% Layer 2
gate(and4, and, w1, w2, w9).
gate(or3, or, w3, w4, w10).
gate(xor4, xor, w5, w6, w11).
gate(and5, and, w2, w7, w12).
gate(or4, or, w8, w5, w13).
gate(not2, neg, w7, none, w14).
gate(xor5, xor, w6, w1, w15).
gate(and6, and, w4, w8, w16).

%% Layer 3
gate(xor6, xor, w9, w10, w17).
gate(and7, and, w11, w12, w18).
gate(or5, or, w13, w14, w19).
gate(xor7, xor, w15, w16, w20).
gate(and8, and, w9, w13, w21).
gate(or6, or, w10, w12, w22).
gate(not3, neg, w11, none, w23).
gate(xor8, xor, w14, w16, w24).

%% Layer 4
gate(and9, and, w17, w18, w25).
gate(or7, or, w19, w20, w26).
gate(xor9, xor, w21, w22, w27).
gate(and10, and, w23, w24, w28).
gate(or8, or, w25, w26, w29).
gate(xor10, xor, w27, w28, w30).
gate(and11, and, w22, w24, w31).
gate(or9, or, w21, w23, w32).

%% Final Stage
gate(xor11, xor, w29, w30, u1).
gate(and12, and, w31, w32, u2).
gate(or10, or, w17, w29, u3).
gate(not4, neg, u2, none, out2).
gate(or11, or, u1, u3, out1).
gate(xor12, xor, w30, w31, out3).

%% Collect all gate names
gate_name(G) :- gate(G, _, _, _, _).

%% ========== WIRE VALUE PROPAGATION ==========
%% Primary inputs get their values from test data
wire_val(In, T, V) :- primary_input(In), test(T), input_val(T, In, V).

%% Correct (raw) output of each gate based on actual input wire values
%% AND gate
raw_val(G, T, 1) :- gate(G, and, In1, In2, _), test(T), wire_val(In1, T, 1), wire_val(In2, T, 1).
raw_val(G, T, 0) :- gate(G, and, In1, In2, _), test(T), wire_val(In1, T, 0).
raw_val(G, T, 0) :- gate(G, and, In1, In2, _), test(T), wire_val(In2, T, 0).

%% OR gate
raw_val(G, T, 1) :- gate(G, or, In1, In2, _), test(T), wire_val(In1, T, 1).
raw_val(G, T, 1) :- gate(G, or, In1, In2, _), test(T), wire_val(In2, T, 1).
raw_val(G, T, 0) :- gate(G, or, In1, In2, _), test(T), wire_val(In1, T, 0), wire_val(In2, T, 0).

%% XOR gate
raw_val(G, T, 1) :- gate(G, xor, In1, In2, _), test(T), wire_val(In1, T, V1), wire_val(In2, T, V2), V1 != V2.
raw_val(G, T, 0) :- gate(G, xor, In1, In2, _), test(T), wire_val(In1, T, V), wire_val(In2, T, V).

%% NEG (NOT) gate
raw_val(G, T, 1) :- gate(G, neg, In, none, _), test(T), wire_val(In, T, 0).
raw_val(G, T, 0) :- gate(G, neg, In, none, _), test(T), wire_val(In, T, 1).

%% ========== FAULT MODELING ==========
%% Choose at most one fault per gate
{ faulty(G, M) : fault_mode(M) } 1 :- gate_name(G).

%% At most 3 gates can be faulty
:- #count { G : faulty(G, _) } > 3.

%% Compute actual output wire value based on fault mode
%% No fault: output equals correct value
wire_val(W, T, V) :- gate(G, _, _, _, W), test(T), raw_val(G, T, V), not faulty(G, _).

%% stuck0: output always 0
wire_val(W, T, 0) :- faulty(G, stuck0), gate(G, _, _, _, W), test(T).

%% stuck1: output always 1
wire_val(W, T, 1) :- faulty(G, stuck1), gate(G, _, _, _, W), test(T).

%% invert: output is flipped
wire_val(W, T, 1-V) :- faulty(G, invert), gate(G, _, _, _, W), test(T), raw_val(G, T, V).

%% open: output can be 0 or 1 (chosen per test)
1 { wire_val(W, T, 0); wire_val(W, T, 1) } 1 :- faulty(G, open), gate(G, _, _, _, W), test(T).

%% ========== OBSERVED OUTPUT CONSTRAINTS ==========
%% All tests produce observed output (out1=0, out2=1, out3=0)
:- test(T), wire_val(out1, T, 1).
:- test(T), wire_val(out2, T, 0).
:- test(T), wire_val(out3, T, 1).

%% ========== OPTIMIZATION ==========
%% Minimize total fault cost
#minimize { C, G, M : faulty(G, M), fault_cost(M, C) }.

%% ========== OUTPUT ==========
#show faulty/2.
#show total_cost/1.

%% Compute total cost for display
total_cost(C) :- C = #sum { Cost, G, M : faulty(G, M), fault_cost(M, Cost) }.