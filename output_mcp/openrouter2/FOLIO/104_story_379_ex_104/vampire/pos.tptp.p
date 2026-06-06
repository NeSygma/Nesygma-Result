fof(premise1, axiom, ! [X] : (born_in_multiple_birth(X) => spends_time_with_siblings(X))).
fof(premise2, axiom, ! [X] : (has_siblings_born_together(X) => born_in_multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains_often(X) => has_siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time_with_siblings(X) => live_at_home(X))).
fof(premise6, axiom, (born_in_multiple_birth(luke) => live_with_strangers(luke))).
fof(premise7, axiom, (live_with_strangers(luke) => born_in_multiple_birth(luke))).
fof(conjecture, conjecture, ~born_in_multiple_birth(luke) & ~complains_often(luke)).