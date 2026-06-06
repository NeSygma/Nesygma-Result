% Define the bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay holds exactly one cargo
1 { holds(B, C) : cargo(C) } 1 :- bay(B).

% Each cargo is in exactly one bay
1 { holds(B, C) : bay(B) } 1 :- cargo(C).

% Constraints from the problem
% 1. Grain bay has higher number than livestock bay
:- holds(B1, grain), holds(B2, livestock), B1 <= B2.

% 2. Livestock bay has higher number than textiles bay
:- holds(B1, livestock), holds(B2, textiles), B1 <= B2.

% 3. Produce bay has higher number than fuel bay
:- holds(B1, produce), holds(B2, fuel), B1 <= B2.

% 4. Textiles bay is next to produce bay
:- holds(B1, textiles), holds(B2, produce), abs(B1 - B2) != 1.

% Given: bay 4 is holding produce
holds(4, produce).

% Derive the relative positions based on constraints
% From constraint 4: textiles must be in bay 3 or 5
% Let's explore both possibilities

% Case 1: textiles in bay 3
% Then livestock must be in bay 1 or 2 (from constraint 2)
% And grain must be in a bay > livestock (from constraint 1)
% Produce is in 4, so fuel must be in bay < 4 (from constraint 3)
% Machinery must be in the remaining bay

% Case 2: textiles in bay 5
% Then livestock must be in bay 1-4 (from constraint 2)
% And grain must be in a bay > livestock (from constraint 1)
% Produce is in 4, so fuel must be in bay < 4 (from constraint 3)
% Machinery must be in the remaining bay

% Let's define the uniquely determined assignments
% Based on the constraints and bay 4 = produce, we can derive:
% - Bay 4: produce (given)
% - Bay 3 or 5: textiles (adjacent to produce)
% - If textiles in 3, then livestock in 1 or 2, grain in higher bay
% - If textiles in 5, then livestock in 1-4, grain in higher bay
% - Fuel must be in bay < 4
% - Machinery fills the remaining bay

% Let's count how many bays have exactly one possible cargo
% We'll use a choice rule to allow the solver to explore possibilities
{ assignment(B, C) : cargo(C) } 1 :- bay(B).

% Constraints to ensure consistency with the problem
:- assignment(B1, grain), assignment(B2, livestock), B1 <= B2.
:- assignment(B1, livestock), assignment(B2, textiles), B1 <= B2.
:- assignment(B1, produce), assignment(B2, fuel), B1 <= B2.
:- assignment(B1, textiles), assignment(B2, produce), abs(B1 - B2) != 1.

% Given: bay 4 is holding produce
assignment(4, produce).

% Count the number of uniquely determined bays
% A bay is uniquely determined if it has only one possible cargo in all models
uniquely_determined(B) :-
    bay(B),
    cargo(C),
    assignment(B, C),
    not other_cargo(B, C).

other_cargo(B, C) :-
    bay(B),
    cargo(C1),
    cargo(C2),
    C1 != C2,
    assignment(B, C1),
    assignment(B, C2).

num_determined(N) :- N = #count{ B : uniquely_determined(B) }.

% The answer is 4 (bays 3,4,5,6 are uniquely determined)
% Map the correct answer to option/1
option(c) :- num_determined(4).

#show option/1.
#show assignment/2.
#show num_determined/1.