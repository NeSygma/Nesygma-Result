% Barutin Cove Problem - Negative Version
% Premises
fof(premise_1, axiom, cove(barutin_cove)).
fof(premise_2, axiom, named_after(barutin_cove, barutin)).
fof(premise_3, axiom, on_coast_of(barutin_cove, snow_island)).
fof(premise_4, axiom, island(snow_island)).
fof(premise_5, axiom, island(greenwich_island)).
fof(premise_6, axiom, island(deception_island)).
fof(premise_7, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise_8, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise_9, axiom, located_in(deception_island, south_shetland_islands)).
fof(premise_10, axiom, located_in(antarctica, south_shetland_islands)).
fof(premise_11, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).

% Distinctness axioms
fof(distinct_1, axiom, barutin_cove != barutin).
fof(distinct_2, axiom, barutin_cove != snow_island).
fof(distinct_3, axiom, barutin_cove != greenwich_island).
fof(distinct_4, axiom, barutin_cove != deception_island).
fof(distinct_5, axiom, barutin_cove != south_shetland_islands).
fof(distinct_6, axiom, barutin_cove != antarctica).
fof(distinct_7, axiom, snow_island != greenwich_island).
fof(distinct_8, axiom, snow_island != deception_island).
fof(distinct_9, axiom, greenwich_island != deception_island).

% Negated conclusion: Barutin Cove is NOT named after all islands in Antarctica
% This means there exists at least one island in Antarctica that Barutin Cove is NOT named after
fof(goal, conjecture, ? [I] : (island(I) & located_in(I, antarctica) & ~named_after(barutin_cove, I))).