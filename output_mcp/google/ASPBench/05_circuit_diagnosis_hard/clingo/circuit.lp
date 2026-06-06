% --- Circuit Definition ---
gate(and1, and, in1, in2, w1). gate(xor1, xor, in3, in4, w2). gate(or1, or, in5, in6, w3). gate(and2, and, in7, in8, w4).
gate(xor2, xor, in9, in10, w5). gate(not1, not, in1, w6). gate(or2, or, in3, in5, w7). gate(and3, and, in4, in6, w8).
gate(and4, and, w1, w2, w9). gate(or3, or, w3, w4, w10). gate(xor4, xor, w5, w6, w11). gate(and5, and, w2, w7, w12).
gate(or4, or, w8, w5, w13). gate(not2, not, w7, w14). gate(xor5, xor, w6, w1, w15). gate(and6, and, w4, w8, w16).
gate(xor6, xor, w9, w10, w17). gate(and7, and, w11, w12, w18). gate(or5, or, w13, w14, w19). gate(xor7, xor, w15, w16, w20).
gate(and8, and, w9, w13, w21). gate(or6, or, w10, w12, w22). gate(not3, not, w11, w23). gate(xor8, xor, w14, w16, w24).
gate(and9, and, w17, w18, w25). gate(or7, or, w19, w20, w26). gate(xor9, xor, w21, w22, w27). gate(and10, and, w23, w24, w28).
gate(or8, or, w25, w26, w29). gate(xor10, xor, w27, w28, w30). gate(and11, and, w22, w24, w31). gate(or9, or, w21, w23, w32).
gate(xor11, xor, w29, w30, u1). gate(and12, and, w31, w32, u2). gate(or10, or, w17, w29, u3). gate(not4, not, u2, out2).
gate(or11, or, u1, u3, out1). gate(xor12, xor, w30, w31, out3).

% --- Test Cases ---
test(1..8).
input(in1, 1, 0, 1, 0, 1, 0, 1, 0). input(in2, 1, 1, 0, 0, 1, 1, 0, 0). input(in3, 0, 1, 1, 0, 1, 0, 0, 1).
input(in4, 1, 0, 1, 1, 1, 0, 1, 0). input(in5, 1, 1, 0, 1, 0, 1, 0, 1). input(in6, 0, 1, 0, 1, 1, 0, 1, 0).
input(in7, 1, 0, 1, 1, 0, 1, 1, 0). input(in8, 0, 1, 1, 0, 0, 1, 0, 1). input(in9, 1, 1, 0, 0, 1, 0, 1, 1).
input(in10, 0, 1, 0, 1, 0, 1, 1, 0).
obs(out1, 0). obs(out2, 1). obs(out3, 0).

val(T, I, V) :- test(T), input(I, V1, V2, V3, V4, V5, V6, V7, V8), (T=1, V=V1; T=2, V=V2; T=3, V=V3; T=4, V=V4; T=5, V=V5; T=6, V=V6; T=7, V=V7; T=8, V=V8).

% --- Fault Modeling ---
fault_cost(stuck0, 1). fault_cost(stuck1, 1). fault_cost(invert, 1). fault_cost(open, 2).
{fault(G, M) : fault_cost(M, _)} 1 :- gate(G, _, _, _, _).
{fault(G, M) : fault_cost(M, _)} 1 :- gate(G, _, _, _).
:- #count { G : fault(G, _) } > 3.

% --- Logic Propagation ---
% Correct logic
correct_val(T, G, 1) :- gate(G, and, I1, I2, _), val(T, I1, 1), val(T, I2, 1).
correct_val(T, G, 0) :- gate(G, and, I1, I2, _), val(T, I1, 0).
correct_val(T, G, 0) :- gate(G, and, I1, I2, _), val(T, I2, 0).
correct_val(T, G, 1) :- gate(G, or, I1, I2, _), val(T, I1, 1).
correct_val(T, G, 1) :- gate(G, or, I1, I2, _), val(T, I2, 1).
correct_val(T, G, 0) :- gate(G, or, I1, I2, _), val(T, I1, 0), val(T, I2, 0).
correct_val(T, G, 1) :- gate(G, xor, I1, I2, _), val(T, I1, V1), val(T, I2, V2), V1 != V2.
correct_val(T, G, 0) :- gate(G, xor, I1, I2, _), val(T, I1, V1), val(T, I2, V2), V1 == V2.
correct_val(T, G, 1) :- gate(G, not, I1, _), val(T, I1, 0).
correct_val(T, G, 0) :- gate(G, not, I1, _), val(T, I1, 1).

% Wire values
val(T, W, V) :- gate(G, _, I1, I2, W), not fault(G, _), correct_val(T, G, V).
val(T, W, V) :- gate(G, _, I1, W), not fault(G, _), correct_val(T, G, V).
val(T, W, 0) :- gate(G, _, _, W), fault(G, stuck0).
val(T, W, 1) :- gate(G, _, _, W), fault(G, stuck1).
val(T, W, V) :- gate(G, _, _, W), fault(G, invert), correct_val(T, G, CV), V = 1-CV.
{val(T, W, 0); val(T, W, 1)} 1 :- gate(G, _, _, W), fault(G, open).

% --- Constraints ---
:- test(T), obs(O, V), not val(T, O, V).

#minimize { C, G : fault(G, M), fault_cost(M, C) }.
#show fault/2.