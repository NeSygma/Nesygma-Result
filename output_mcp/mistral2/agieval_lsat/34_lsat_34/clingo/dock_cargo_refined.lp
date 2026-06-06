% Base facts: bays and cargo types
bay(1..6).
cargo(fuel; grain; livestock; machinery; produce; textiles).

% Assign each bay to a unique cargo
1 { assignment(B, C) : cargo(C) } 1 :- bay(B).
:- assignment(B1, C), assignment(B2, C), B1 != B2.

% Constraints from the problem statement
% 1. The bay holding grain has a higher number than the bay holding livestock.
:- assignment(B_grain, grain), assignment(B_livestock, livestock), B_grain <= B_livestock.

% 2. The bay holding livestock has a higher number than the bay holding textiles.
:- assignment(B_livestock, livestock), assignment(B_textiles, textiles), B_livestock <= B_textiles.

% 3. The bay holding produce has a higher number than the bay holding fuel.
:- assignment(B_produce, produce), assignment(B_fuel, fuel), B_produce <= B_fuel.

% 4. The bay holding textiles is next to the bay holding produce.
next_to(B1, B2) :- bay(B1), bay(B2), B1 = B2 - 1.
next_to(B1, B2) :- bay(B1), bay(B2), B1 = B2 + 1.

:- assignment(B_textiles, textiles), assignment(B_produce, produce), not next_to(B_textiles, B_produce).

% Helper predicates to identify the bays for each cargo
assignment_fuel(B) :- assignment(B, fuel).
assignment_grain(B) :- assignment(B, grain).
assignment_livestock(B) :- assignment(B, livestock).
assignment_machinery(B) :- assignment(B, machinery).
assignment_produce(B) :- assignment(B, produce).
assignment_textiles(B) :- assignment(B, textiles).

% Define the adjacency for the options
% (A) The bay holding fuel is next to the bay holding machinery.
option_a_impossible :- assignment_fuel(B_fuel), assignment_machinery(B_machinery), not next_to(B_fuel, B_machinery).

% (B) The bay holding grain is next to the bay holding machinery.
option_b_impossible :- assignment_grain(B_grain), assignment_machinery(B_machinery), not next_to(B_grain, B_machinery).

% (C) The bay holding livestock is next to the bay holding fuel.
option_c_impossible :- assignment_livestock(B_livestock), assignment_fuel(B_fuel), not next_to(B_livestock, B_fuel).

% (D) The bay holding produce is next to the bay holding livestock.
option_d_impossible :- assignment_produce(B_produce), assignment_livestock(B_livestock), not next_to(B_produce, B_livestock).

% (E) The bay holding textiles is next to the bay holding fuel.
option_e_impossible :- assignment_textiles(B_textiles), assignment_fuel(B_fuel), not next_to(B_textiles, B_fuel).

% The correct answer is the option that is impossible in all models
answer(a) :- option_a_impossible, not option_b_impossible, not option_c_impossible, not option_d_impossible, not option_e_impossible.
answer(b) :- option_b_impossible, not option_a_impossible, not option_c_impossible, not option_d_impossible, not option_e_impossible.
answer(c) :- option_c_impossible, not option_a_impossible, not option_b_impossible, not option_d_impossible, not option_e_impossible.
answer(d) :- option_d_impossible, not option_a_impossible, not option_b_impossible, not option_c_impossible, not option_e_impossible.
answer(e) :- option_e_impossible, not option_a_impossible, not option_b_impossible, not option_c_impossible, not option_d_impossible.

#show answer/1.