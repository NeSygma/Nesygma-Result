fof(p1, axiom, ! [X] : (multiple_birth(X) => spend_time_with_siblings(X))).
fof(p2, axiom, ! [X] : (have_sibling_born_together(X) => multiple_birth(X))).
fof(p3, axiom, ! [X] : (complain_annoying_siblings(X) => have_sibling_born_together(X))).
fof(p4, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(p5, axiom, ! [X] : (spend_time_with_siblings(X) => live_at_home(X))).
fof(p6, axiom, ( (multiple_birth(luke) & live_with_strangers(luke)) | (~multiple_birth(luke) & ~live_with_strangers(luke)) )).
fof(goal, conjecture, ~complain_annoying_siblings(luke)).