% Gates and their types
gate(and1, and).   gate(xor1, xor).   gate(or1, or).    gate(and2, and).
gate(xor2, xor).   gate(not1, not).   gate(or2, or).    gate(and3, and).
gate(and4, and).   gate(or3, or).     gate(xor4, xor).  gate(and5, and).
gate(or4, or).     gate(not2, not).   gate(xor5, xor).  gate(and6, and).
gate(xor6, xor).   gate(and7, and).   gate(or5, or).    gate(xor7, xor).
gate(and8, and).   gate(or6, or).     gate(not3, not).  gate(xor8, xor).
gate(and9, and).   gate(or7, or).     gate(xor9, xor).  gate(and10, and).
gate(or8, or).     gate(xor10, xor).  gate(and11, and).  gate(or9, or).
gate(xor11, xor).  gate(and12, and).  gate(or10, or).   gate(not4, not).
gate(or11, or).    gate(xor12, xor).

% Inputs and outputs for each gate
input(and1, in1).   input(and1, in2).   output(and1, w1).
input(xor1, in3).   input(xor1, in4).   output(xor1, w2).
input(or1, in5).    input(or1, in6).    output(or1, w3).
input(and2, in7).   input(and2, in8).   output(and2, w4).
input(xor2, in9).   input(xor2, in10).  output(xor2, w5).
input(not1, in1).   output(not1, w6).
input(or2, in3).    input(or2, in5).    output(or2, w7).
input(and3, in4).   input(and3, in6).   output(and3, w8).

input(and4, w1).    input(and4, w2).    output(and4, w9).
input(or3, w3).     input(or3, w4).     output(or3, w10).
input(xor4, w5).    input(xor4, w6).    output(xor4, w11).
input(and5, w2).    input(and5, w7).    output(and5, w12).
input(or4, w8).     input(or4, w5).     output(or4, w13).
input(not2, w7).    output(not2, w14).
input(xor5, w6).    input(xor5, w1).    output(xor5, w15).
input(and6, w4).    input(and6, w8).    output(and6, w16).

input(xor6, w9).    input(xor6, w10).   output(xor6, w17).
input(and7, w11).   input(and7, w12).   output(and7, w18).
input(or5, w13).    input(or5, w14).    output(or5, w19).
input(xor7, w15).   input(xor7, w16).   output(xor7, w20).
input(and8, w9).    input(and8, w13).   output(and8, w21).
input(or6, w10).    input(or6, w12).    output(or6, w22).
input(not3, w11).   output(not3, w23).
input(xor8, w14).   input(xor8, w16).   output(xor8, w24).

input(and9, w17).   input(and9, w18).   output(and9, w25).
input(or7, w19).    input(or7, w20).    output(or7, w26).
input(xor9, w21).   input(xor9, w22).   output(xor9, w27).
input(and10, w23).  input(and10, w24).  output(and10, w28).
input(or8, w25).    input(or8, w26).    output(or8, w29).
input(xor10, w27).  input(xor10, w28).  output(xor10, w30).
input(and11, w22).  input(and11, w24).  output(and11, w31).
input(or9, w21).    input(or9, w23).    output(or9, w32).

input(xor11, w29).  input(xor11, w30).  output(xor11, u1).
input(and12, w31).  input(and12, w32).  output(and12, u2).
input(or10, w17).   input(or10, w29).   output(or10, u3).
input(not4, u2).    output(not4, out2).
input(or11, u1).    input(or11, u3).    output(or11, out1).
input(xor12, w30).  input(xor12, w31).  output(xor12, out3).

% Primary inputs and outputs
primary_input(in1).   primary_input(in2).   primary_input(in3).
primary_input(in4).   primary_input(in5).   primary_input(in6).
primary_input(in7).   primary_input(in8).   primary_input(in9).
primary_input(in10).

primary_output(out1). primary_output(out2). primary_output(out3).

% Wires
wire(in1).   wire(in2).   wire(in3).   wire(in4).   wire(in5).
wire(in6).   wire(in7).   wire(in8).   wire(in9).   wire(in10).
wire(w1).    wire(w2).    wire(w3).    wire(w4).    wire(w5).
wire(w6).    wire(w7).    wire(w8).    wire(w9).    wire(w10).
wire(w11).   wire(w12).   wire(w13).   wire(w14).   wire(w15).
wire(w16).   wire(w17).   wire(w18).   wire(w19).   wire(w20).
wire(w21).   wire(w22).   wire(w23).   wire(w24).   wire(w25).
wire(w26).   wire(w27).   wire(w28).   wire(w29).   wire(w30).
wire(w31).   wire(w32).   wire(u1).    wire(u2).    wire(u3).
wire(out1).  wire(out2).  wire(out3).

% Test cases
test(1..8).

% Input values for each test
input_value(1, in1, 1). input_value(1, in2, 1). input_value(1, in3, 0).
input_value(1, in4, 1). input_value(1, in5, 1). input_value(1, in6, 0).
input_value(1, in7, 1). input_value(1, in8, 0). input_value(1, in9, 1).
input_value(1, in10, 0).

input_value(2, in1, 0). input_value(2, in2, 1). input_value(2, in3, 1).
input_value(2, in4, 0). input_value(2, in5, 1). input_value(2, in6, 1).
input_value(2, in7, 0). input_value(2, in8, 1). input_value(2, in9, 1).
input_value(2, in10, 1).

input_value(3, in1, 1). input_value(3, in2, 0). input_value(3, in3, 1).
input_value(3, in4, 1). input_value(3, in5, 0). input_value(3, in6, 0).
input_value(3, in7, 1). input_value(3, in8, 1). input_value(3, in9, 0).
input_value(3, in10, 0).

input_value(4, in1, 0). input_value(4, in2, 0). input_value(4, in3, 0).
input_value(4, in4, 1). input_value(4, in5, 1). input_value(4, in6, 1).
input_value(4, in7, 1). input_value(4, in8, 0). input_value(4, in9, 0).
input_value(4, in10, 1).

input_value(5, in1, 1). input_value(5, in2, 1). input_value(5, in3, 1).
input_value(5, in4, 1). input_value(5, in5, 0). input_value(5, in6, 1).
input_value(5, in7, 0). input_value(5, in8, 0). input_value(5, in9, 1).
input_value(5, in10, 0).

input_value(6, in1, 0). input_value(6, in2, 1). input_value(6, in3, 0).
input_value(6, in4, 0). input_value(6, in5, 1). input_value(6, in6, 0).
input_value(6, in7, 1). input_value(6, in8, 1). input_value(6, in9, 0).
input_value(6, in10, 1).

input_value(7, in1, 1). input_value(7, in2, 0). input_value(7, in3, 0).
input_value(7, in4, 1). input_value(7, in5, 0). input_value(7, in6, 1).
input_value(7, in7, 1). input_value(7, in8, 0). input_value(7, in9, 1).
input_value(7, in10, 1).

input_value(8, in1, 0). input_value(8, in2, 0). input_value(8, in3, 1).
input_value(8, in4, 0). input_value(8, in5, 1). input_value(8, in6, 0).
input_value(8, in7, 0). input_value(8, in8, 1). input_value(8, in9, 1).
input_value(8, in10, 0).

% Observed outputs for each test
observed_output(1, out1, 0). observed_output(1, out2, 1). observed_output(1, out3, 0).
observed_output(2, out1, 0). observed_output(2, out2, 1). observed_output(2, out3, 0).
observed_output(3, out1, 0). observed_output(3, out2, 1). observed_output(3, out3, 0).
observed_output(4, out1, 0). observed_output(4, out2, 1). observed_output(4, out3, 0).
observed_output(5, out1, 0). observed_output(5, out2, 1). observed_output(5, out3, 0).
observed_output(6, out1, 0). observed_output(6, out2, 1). observed_output(6, out3, 0).
observed_output(7, out1, 0). observed_output(7, out2, 1). observed_output(7, out3, 0).
observed_output(8, out1, 0). observed_output(8, out2, 1). observed_output(8, out3, 0).

% Fault modes and costs
fault_mode(stuck0). fault_mode(stuck1). fault_mode(invert). fault_mode(open).
fault_cost(stuck0, 1). fault_cost(stuck1, 1). fault_cost(invert, 1). fault_cost(open, 2).

% Choice of faulty gates (at most 3)
{ faulty(G, F) : fault_mode(F) } <= 3 :- gate(G, _).

% Mutually exclusive fault modes for a gate
:- faulty(G, F1), faulty(G, F2), F1 != F2.

% Wire values for primary inputs
wire_value(W, T, V) :- primary_input(W), input_value(T, W, V).

% Propagate wire values through gates
% AND gate
wire_value(W, T, V) :-
    output(G, W),
    gate(G, and),
    input(G, I1),
    input(G, I2),
    wire_value(I1, T, V1),
    wire_value(I2, T, V2),
    V = V1 * V2,
    not faulty(G, _).

wire_value(W, T, 0) :- output(G, W), faulty(G, stuck0).
wire_value(W, T, 1) :- output(G, W), faulty(G, stuck1).

wire_value(W, T, V) :-
    output(G, W),
    gate(G, and),
    faulty(G, invert),
    input(G, I1),
    input(G, I2),
    wire_value(I1, T, V1),
    wire_value(I2, T, V2),
    V12 = V1 * V2,
    V = 1 - V12.

% XOR gate
wire_value(W, T, V) :-
    output(G, W),
    gate(G, xor),
    input(G, I1),
    input(G, I2),
    wire_value(I1, T, V1),
    wire_value(I2, T, V2),
    V = (V1 + V2) mod 2,
    not faulty(G, _).

wire_value(W, T, 0) :- output(G, W), faulty(G, stuck0).
wire_value(W, T, 1) :- output(G, W), faulty(G, stuck1).

wire_value(W, T, V) :-
    output(G, W),
    gate(G, xor),
    faulty(G, invert),
    input(G, I1),
    input(G, I2),
    wire_value(I1, T, V1),
    wire_value(I2, T, V2),
    V12 = (V1 + V2) mod 2,
    V = 1 - V12.

% OR gate
wire_value(W, T, V) :-
    output(G, W),
    gate(G, or),
    input(G, I1),
    input(G, I2),
    wire_value(I1, T, V1),
    wire_value(I2, T, V2),
    V = min(1, V1 + V2),
    not faulty(G, _).

wire_value(W, T, 0) :- output(G, W), faulty(G, stuck0).
wire_value(W, T, 1) :- output(G, W), faulty(G, stuck1).

wire_value(W, T, V) :-
    output(G, W),
    gate(G, or),
    faulty(G, invert),
    input(G, I1),
    input(G, I2),
    wire_value(I1, T, V1),
    wire_value(I2, T, V2),
    V12 = min(1, V1 + V2),
    V = 1 - V12.

% NOT gate
wire_value(W, T, V) :-
    output(G, W),
    gate(G, not),
    input(G, I1),
    wire_value(I1, T, V1),
    V = 1 - V1,
    not faulty(G, _).

wire_value(W, T, 0) :- output(G, W), faulty(G, stuck0).
wire_value(W, T, 1) :- output(G, W), faulty(G, stuck1).

wire_value(W, T, V) :-
    output(G, W),
    gate(G, not),
    faulty(G, invert),
    input(G, I1),
    wire_value(I1, T, V1),
    V1n = 1 - V1,
    V = 1 - V1n.

% Open fault: arbitrary value (0 or 1)
{ wire_value(W, T, 0); wire_value(W, T, 1) } = 1 :-
    output(G, W),
    faulty(G, open).

% Ensure primary outputs match observed outputs
:- primary_output(O), observed_output(T, O, V), not wire_value(O, T, V).

% Minimize total cost
total_cost(C) :- C = #sum { Cost : faulty(G, F), fault_cost(F, Cost) }.
#minimize { total_cost(C) }.

% Show the diagnosis
#show faulty/2.
#show total_cost/1.