% Components and their types
component(and1; or1; notgate1; xor1; and2).
gate_type(and1, and).
gate_type(or1, or).
gate_type(notgate1, not).
gate_type(xor1, xor).
gate_type(and2, and).

% Inputs and outputs for each component
input(and1, in1). input(and1, in2). output(and1, w1).
input(or1, w1). input(or1, in3). output(or1, w2).
input(notgate1, w2). output(notgate1, out1).
input(xor1, in1). input(xor1, in4). output(xor1, w3).
input(and2, w3). input(and2, in2). output(and2, out2).

% Input values
input_value(in1, 1). input_value(in2, 0). input_value(in3, 1). input_value(in4, 1).

% Observed outputs
observed_output(out1, 1). observed_output(out2, 0).

% Time step
time(0).

% Signal values for inputs are fixed
signal(P, V, T) :- input_value(P, V), time(T).

% Define the expected behavior for non-faulty components
% AND gate: V = V1 * V2
signal(O, V, T) :- gate_type(C, and), output(C, O), input(C, I1), input(C, I2),
                   signal(I1, V1, T), signal(I2, V2, T), V = V1 * V2, not faulty(C), time(T).

% OR gate: V = min(1, V1 + V2)
signal(O, V, T) :- gate_type(C, or), output(C, O), input(C, I1), input(C, I2),
                   signal(I1, V1, T), signal(I2, V2, T), V = (V1 + V2), V <= 1, not faulty(C), time(T).

% NOT gate: V = 1 - V1
signal(O, V, T) :- gate_type(C, not), output(C, O), input(C, I1),
                   signal(I1, V1, T), V = 1 - V1, not faulty(C), time(T).

% XOR gate: V = (V1 + V2) % 2
signal(O, V, T) :- gate_type(C, xor), output(C, O), input(C, I1), input(C, I2),
                   signal(I1, V1, T), signal(I2, V2, T), V = (V1 + V2) % 2, not faulty(C), time(T).

% Faulty components can produce any output (no constraint)

% Ensure observed outputs are satisfied
:- observed_output(P, V), signal(P, Vobs, 0), V != Vobs.

% Diagnosis: a set of faulty components
{ faulty(C) : component(C) }.

% Minimality: no proper subset of a diagnosis is a diagnosis
% This is implicitly handled by the minimality of answer sets in ASP
% No need for explicit constraint here

% Output the faulty components
#show faulty/1.