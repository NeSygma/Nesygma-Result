% Define the components and their types
component(and1; or1; notgate1; xor1; and2).

% Define the types of components
type(and1, and).
type(or1, or).
type(notgate1, not).
type(xor1, xor).
type(and2, and).

% Define the connections: gate(Input1, Input2, Output) for binary gates, gate(Input, Output) for unary gates
connection(and1, in1, in2, w1).
connection(or1, w1, in3, w2).
connection(notgate1, w2, out1).
connection(xor1, in1, in4, w3).
connection(and2, w3, in2, out2).

% Input values
input(in1, 1).
input(in2, 0).
input(in3, 1).
input(in4, 1).

% Expected outputs (if all components are working correctly)
expected(out1, 0).
expected(out2, 0).

% Observed outputs
observed(out1, 1).
observed(out2, 0).

% A component is faulty if it is assumed to be faulty
faulty(C) :- component(C), assumed_faulty(C).

% A component is working correctly if it is not assumed to be faulty
working(C) :- component(C), not faulty(C).

% Define the correct behavior of each gate type when working correctly
% AND gate: output is 1 if both inputs are 1, else 0
correct_output(G, O, 1) :-
    type(G, and),
    connection(G, I1, I2, O),
    input(I1, 1),
    input(I2, 1),
    working(G).

correct_output(G, O, 0) :-
    type(G, and),
    connection(G, I1, I2, O),
    (input(I1, 0); input(I2, 0)),
    working(G).

% OR gate: output is 1 if at least one input is 1, else 0
correct_output(G, O, 1) :-
    type(G, or),
    connection(G, I1, I2, O),
    (input(I1, 1); input(I2, 1)),
    working(G).

correct_output(G, O, 0) :-
    type(G, or),
    connection(G, I1, I2, O),
    input(I1, 0),
    input(I2, 0),
    working(G).

% NOT gate: output is 1 if input is 0, else 0
correct_output(G, O, 1) :-
    type(G, not),
    connection(G, I, O),
    input(I, 0),
    working(G).

correct_output(G, O, 0) :-
    type(G, not),
    connection(G, I, O),
    input(I, 1),
    working(G).

% XOR gate: output is 1 if inputs are different, else 0
correct_output(G, O, 1) :-
    type(G, xor),
    connection(G, I1, I2, O),
    input(I1, 1), input(I2, 0).

correct_output(G, O, 1) :-
    type(G, xor),
    connection(G, I1, I2, O),
    input(I1, 0), input(I2, 1).

correct_output(G, O, 0) :-
    type(G, xor),
    connection(G, I1, I2, O),
    input(I1, 0), input(I2, 0).

correct_output(G, O, 0) :-
    type(G, xor),
    connection(G, I1, I2, O),
    input(I1, 1), input(I2, 1).

% Actual output: if the component is faulty, it can produce any output
% If working, it must produce the correct output
actual_output(O, V) :-
    correct_output(_, O, V),
    working(_).

% For faulty components, allow any output (non-deterministic)
{ actual_output(O, 0; actual_output(O, 1) } :-
    connection(_, _, _, O),
    faulty(_).

% The diagnosis is valid if the actual outputs match the observed outputs
:- observed(O, V), not actual_output(O, V).

% Minimality: prefer smaller sets of faulty components
#minimize { 1@1,C : assumed_faulty(C) }.

% Generate all possible sets of faulty components (diagnoses)
{ assumed_faulty(C) : component(C) }.

% Show the faulty components in the diagnosis
#show assumed_faulty/1.

% Explanation
explanation("All minimal sets of faulty components that explain the observed outputs.").
#show explanation/1.