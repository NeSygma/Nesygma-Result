% Digital Circuit Diagnosis Problem

% Define components
component(and1).
component(or1).
component(notgate1).
component(xor1).
component(and2).

% Define inputs and outputs
input(in1).
input(in2).
input(in3).
input(in4).
output(out1).
output(out2).

% Define internal wires
wire(w1).
wire(w2).
wire(w3).

% Input values for this test case
input_value(in1, 1).
input_value(in2, 0).
input_value(in3, 1).
input_value(in4, 1).

% Expected and observed outputs
expected_output(out1, 0).
expected_output(out2, 0).
observed_output(out1, 1).
observed_output(out2, 0).

% Faulty components - choice rule to consider any subset as potentially faulty
{ faulty(C) } :- component(C).

% For faulty components, we can choose any output value
% We'll use a helper predicate to represent gate outputs
gate_output(G, V) :- faulty(G), V = 0.
gate_output(G, V) :- faulty(G), V = 1.

% For correct components, output is determined by gate logic
% AND gate (and1)
gate_output(and1, 1) :- not faulty(and1), input_value(in1, 1), input_value(in2, 1).
gate_output(and1, 0) :- not faulty(and1), (input_value(in1, 0); input_value(in2, 0)).

% OR gate (or1)
gate_output(or1, 1) :- not faulty(or1), (value(w1, 1); input_value(in3, 1)).
gate_output(or1, 0) :- not faulty(or1), value(w1, 0), input_value(in3, 0).

% NOT gate (notgate1)
gate_output(notgate1, 1) :- not faulty(notgate1), value(w2, 0).
gate_output(notgate1, 0) :- not faulty(notgate1), value(w2, 1).

% XOR gate (xor1)
gate_output(xor1, 1) :- not faulty(xor1), input_value(in1, V1), input_value(in4, V2), V1 != V2.
gate_output(xor1, 0) :- not faulty(xor1), input_value(in1, V1), input_value(in4, V2), V1 = V2.

% AND gate (and2)
gate_output(and2, 1) :- not faulty(and2), value(w3, 1), input_value(in2, 1).
gate_output(and2, 0) :- not faulty(and2), (value(w3, 0); input_value(in2, 0)).

% Define wire values from gate outputs
value(w1, V) :- gate_output(and1, V).
value(w2, V) :- gate_output(or1, V).
value(w3, V) :- gate_output(xor1, V).
value(out1, V) :- gate_output(notgate1, V).
value(out2, V) :- gate_output(and2, V).

% Constraints: observed outputs must match
:- value(out1, V), observed_output(out1, Obs), V != Obs.
:- value(out2, V), observed_output(out2, Obs), V != Obs.

% Find all diagnoses (sets of faulty components that explain observations)
diagnosis(S) :- S = { C : faulty(C) }.

% For minimality: a diagnosis is minimal if no proper subset is also a diagnosis
% We'll use a constraint to eliminate non-minimal sets

% A diagnosis is non-minimal if there exists a proper subset that is also a diagnosis
% We need to check for each diagnosis S, if there exists a component C in S
% such that S \ {C} is also a diagnosis

% To check this, we need to see if there's an assignment where only S \ {C} are faulty
% and observations still hold

% This is complex. Let me use a different approach:

% We'll enumerate all possible faulty sets and check minimality
% by ensuring that for each component in the set, removing it makes the set invalid

% We'll use a helper predicate to mark minimal diagnoses
minimal_diagnosis(S) :- 
    diagnosis(S),
    not non_minimal(S).

% A diagnosis S is non-minimal if there exists a component C in S
% such that there exists an assignment where C is not faulty but observations still hold
non_minimal(S) :-
    diagnosis(S),
    faulty(C),
    S != {C},  % S has more than one component
    % Check if there's an assignment where C is not faulty but observations hold
    % This requires checking if we can "turn off" C and still satisfy constraints
    % We'll do this by checking if there's a model where C is not faulty
    % but all other components in S are faulty, and observations hold

% Actually, this is getting too complex. Let me use a simpler approach:

% Since we have only 5 components, let's enumerate all possible faulty sets
% and check which are minimal by comparing with all other sets

% We'll use a predicate diagnosis_id(N) where N is 0-31
% and map N to components

% But let me try a different approach: use the ASP solver's ability to find all models
% and then we can analyze them

% Actually, let me just run the code and see what diagnoses we get
% Then we can manually check which are minimal

% I'll add #show directives to see the results

#show faulty/1.
#show gate_output/2.
#show value/2.
#show diagnosis/1.

% Also show the final outputs for debugging
#show final_out1/1.
#show final_out2/1.

final_out1(V) :- value(out1, V).
final_out2(V) :- value(out2, V).