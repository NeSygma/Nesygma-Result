% Positive version: original claim as conjecture
% There is at least one cove in Antarctica named after a place in Bulgaria.

% Premises
fof(premise_1, axiom, named_after(barutin_cove, barutin)).
fof(premise_2, axiom, cove(barutin_cove)).
fof(premise_3, axiom, located_in(barutin_cove, southwest_coast_snow_island)).
fof(premise_4, axiom, located_in(southwest_coast_snow_island, snow_island)).
fof(premise_5, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise_6, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise_7, axiom, located_in(deception_island, south_shetland_islands)).
fof(premise_8, axiom, located_in(antarctica, south_shetland_islands)).
fof(premise_9, axiom, place(barutin)).
fof(premise_10, axiom, place(barutin_cove)).
fof(premise_11, axiom, place(southwest_coast_snow_island)).
fof(premise_12, axiom, place(snow_island)).
fof(premise_13, axiom, place(greenwich_island)).
fof(premise_14, axiom, place(deception_island)).
fof(premise_15, axiom, place(south_shetland_islands)).
fof(premise_16, axiom, place(antarctica)).

% Transitivity of located_in
fof(transitivity, axiom, ! [A, B, C] : ((located_in(A, B) & located_in(B, C)) => located_in(A, C))).

% Barutin is a place in Bulgaria
fof(premise_17, axiom, place_in(barutin, bulgaria)).
fof(premise_18, axiom, place(bulgaria)).

% Conclusion: There is at least one cove in Antarctica named after a place in Bulgaria.
% Formalized: ? [C, P] : (cove(C) & located_in(C, antarctica) & named_after(C, P) & place_in(P, bulgaria))
fof(goal, conjecture, ? [C, P] : (cove(C) & located_in(C, antarctica) & named_after(C, P) & place_in(P, bulgaria))).