% Facts
cove(barutin_cove).
named_after(barutin_cove, barutin).
location(barutin_cove, snow_island).
location(snow_island, south_shetland_islands).
location(south_shetland_islands, antarctica).
location(greenwich_island, south_shetland_islands).
location(deception_island, south_shetland_islands).
location(barutin, bulgaria).

% Transitivity of location
location(A,C) :- location(A,B), location(B,C).

% Conclusion true: there exists a cove in Antarctica named after a place in Bulgaria
conclusion_true :- cove(C), location(C, antarctica), named_after(C, P), location(P, bulgaria).

% Conclusion false: never true in this knowledge base
conclusion_false :- false.

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.