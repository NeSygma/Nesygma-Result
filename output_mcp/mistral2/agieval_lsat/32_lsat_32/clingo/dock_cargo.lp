% Define the bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Assign each bay a unique cargo
1 { assignment(Bay, Cargo) : cargo(Cargo) } 1 :- bay(Bay).
:- assignment(B1, C1), assignment(B2, C2), B1 != B2, C1 == C2.

% Constraints from the problem
% 1. The bay holding grain has a higher number than the bay holding livestock.
:- assignment(B_grain, grain), assignment(B_livestock, livestock), B_grain =< B_livestock.

% 2. The bay holding livestock has a higher number than the bay holding textiles.
:- assignment(B_livestock, livestock), assignment(B_textiles, textiles), B_livestock =< B_textiles.

% 3. The bay holding produce has a higher number than the bay holding fuel.
:- assignment(B_produce, produce), assignment(B_fuel, fuel), B_produce =< B_fuel.

% 4. The bay holding textiles is next to the bay holding produce.
:- assignment(B_textiles, textiles), assignment(B_produce, produce), not (B_textiles = B_produce - 1 ; B_textiles = B_produce + 1).

% Additional constraint: Exactly one bay between machinery and grain
% This means |B_machinery - B_grain| = 2
:- assignment(B_machinery, machinery), assignment(B_grain, grain), not (B_machinery = B_grain - 2 ; B_machinery = B_grain + 2).

% Count the number of bays with determined cargo
% A bay's cargo is determined if it is the only possible cargo for that bay given the constraints

% Helper to count determined bays
determined_bay(Bay) :-
    bay(Bay),
    cargo(Cargo),
    assignment(Bay, Cargo),
    not (cargo(OtherCargo), OtherCargo != Cargo, assignment(Bay, OtherCargo)).

% Count the number of determined bays
num_determined(N) :- N = #count { Bay : determined_bay(Bay) }.

% Map the correct answer to option/1
% We need to check the value of N and map it to the correct option

% The problem asks: for exactly how many of the six bays is the type of cargo determined?
% We will check the value of N and map it to the correct option

option(a) :- num_determined(2).
option(b) :- num_determined(3).
option(c) :- num_determined(4).
option(d) :- num_determined(5).
option(e) :- num_determined(6).

#show option/1.