% Base facts: bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Each bay holds exactly one cargo type
1 { holds(B, C) : cargo(C) } 1 :- bay(B).

% Each cargo type is held by exactly one bay
1 { holds(B, C) : bay(B) } 1 :- cargo(C).

% Constraints from the problem statement
% 1. The bay holding grain has a higher number than the bay holding livestock.
:- holds(B1, grain), holds(B2, livestock), B1 <= B2.

% 2. The bay holding livestock has a higher number than the bay holding textiles.
:- holds(B2, livestock), holds(B3, textiles), B2 <= B3.

% 3. The bay holding produce has a higher number than the bay holding fuel.
:- holds(B4, produce), holds(B5, fuel), B4 <= B5.

% 4. The bay holding textiles is next to the bay holding produce.
:- holds(B6, textiles), holds(B7, produce), not (B6 = B7 - 1 ; B6 = B7 + 1).

% Additional constraint: If the bay holding produce is next to the bay holding livestock, then...
% This is a conditional constraint. We will model it as a rule that must hold when the condition is true.

% Helper predicate: produce is next to livestock
produce_next_to_livestock :- holds(B_produce, produce), holds(B_livestock, livestock), (B_produce = B_livestock - 1 ; B_produce = B_livestock + 1).

% --- Define the options as potential facts ---
% We will check which of the options can be true under the given constraints.

% Option A: Bay 2 is holding fuel.
option(a) :- holds(2, fuel), produce_next_to_livestock.

% Option B: Bay 4 is holding produce.
option(b) :- holds(4, produce), produce_next_to_livestock.

% Option C: Bay 4 is holding textiles.
option(c) :- holds(4, textiles), produce_next_to_livestock.

% Option D: Bay 5 is holding grain.
option(d) :- holds(5, grain), produce_next_to_livestock.

% Option E: Bay 5 is holding machinery.
option(e) :- holds(5, machinery), produce_next_to_livestock.

#show option/1.