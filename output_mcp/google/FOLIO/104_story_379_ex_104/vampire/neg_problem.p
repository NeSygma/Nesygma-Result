fof(p1, axiom, ! [X] : (multiple_birth(X) => spends_time_with_siblings(X))).
fof(p2, axiom, ! [X] : (has_siblings_born_together(X) => multiple_birth(X))).
fof(p3, axiom, ! [X] : (complains_about_siblings(X) => has_siblings_born_together(X))).
fof(p4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(p5, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).
fof(p6, axiom, (multiple_birth(luke) & lives_with_strangers(luke)) | (~multiple_birth(luke) & ~lives_with_strangers(luke))).
fof(goal, conjecture, ~ (~multiple_birth(luke) & ~complains_about_siblings(luke))).