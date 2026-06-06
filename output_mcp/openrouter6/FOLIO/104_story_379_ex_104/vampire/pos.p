fof(premise1, axiom, ! [X] : (born_multiple_birth(X) => spends_time_with_siblings(X))).
fof(premise2, axiom, ! [X] : (has_siblings_born_together(X) => born_multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains_about_annoying_siblings(X) => has_siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).
fof(premise6, axiom, (born_multiple_birth(luke) & lives_with_strangers(luke)) | (~born_multiple_birth(luke) & ~lives_with_strangers(luke))).
fof(conclusion, conjecture, (~born_multiple_birth(luke) & ~complains_about_annoying_siblings(luke))).