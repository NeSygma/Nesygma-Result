fof(distinct_places, axiom, (barutin_cove != snow_island & barutin_cove != greenwich_island & barutin_cove != deception_island & barutin_cove != antarctica & barutin_cove != barutin & snow_island != greenwich_island & snow_island != deception_island & snow_island != antarctica & snow_island != barutin & greenwich_island != deception_island & greenwich_island != antarctica & greenwich_island != barutin & deception_island != antarctica & deception_island != barutin & antarctica != barutin)).
fof(premise_1, axiom, cove(barutin_cove)).
fof(premise_2, axiom, named_after(barutin_cove, barutin)).
fof(premise_3, axiom, bulgarian_place(barutin)).
fof(premise_4, axiom, located_in(barutin_cove, snow_island)).
fof(premise_5, axiom, located_in(snow_island, south_shetland_islands)).
fof(premise_6, axiom, located_in(greenwich_island, south_shetland_islands)).
fof(premise_7, axiom, located_in(deception_island, south_shetland_islands)).
fof(premise_8, axiom, located_in(antarctica, south_shetland_islands)).
fof(premise_9, axiom, ! [A,B,C] : ((located_in(A,B) & located_in(B,C)) => located_in(A,C))).
fof(goal, conjecture, ~(? [X,Y] : (cove(X) & located_in(X, antarctica) & named_after(X,Y) & bulgarian_place(Y)))).