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

% Define the adjacency for the options
% (A) The bay holding fuel is next to the bay holding machinery.
option_a_holds :- assignment(B_fuel, fuel), assignment(B_machinery, machinery), next_to(B_fuel, B_machinery).

% (B) The bay holding grain is next to the bay holding machinery.
option_b_holds :- assignment(B_grain, grain), assignment(B_machinery, machinery), next_to(B_grain, B_machinery).

% (C) The bay holding livestock is next to the bay holding fuel.
option_c_holds :- assignment(B_livestock, livestock), assignment(B_fuel, fuel), next_to(B_livestock, B_fuel).

% (D) The bay holding produce is next to the bay holding livestock.
option_d_holds :- assignment(B_produce, produce), assignment(B_livestock, livestock), next_to(B_produce, B_livestock).

% (E) The bay holding textiles is next to the bay holding fuel.
option_e_holds :- assignment(B_textiles, textiles), assignment(B_fuel, fuel), next_to(B_textiles, B_fuel).

% Check which options are possible
possible_a :- option_a_holds.
possible_b :- option_b_holds.
possible_c :- option_c_holds.
possible_d :- option_d_holds.
possible_e :- option_e_holds.

% The correct answer is the option that is NOT possible
option(a) :- not possible_a, possible_b, possible_c, possible_d, possible_e.
option(b) :- not possible_b, possible_a, possible_c, possible_d, possible_e.
option(c) :- not possible_c, possible_a, possible_b, possible_d, possible_e.
option(d) :- not possible_d, possible_a, possible_b, possible_c, possible_e.
option(e) :- not possible_e, possible_a, possible_b, possible_c, possible_d.

#show option/1.