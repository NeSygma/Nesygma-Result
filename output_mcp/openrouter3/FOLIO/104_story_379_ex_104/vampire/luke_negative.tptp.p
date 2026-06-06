% Luke's logical problem - Negative version (negated conclusion as conjecture)
fof(born_multiple_birth_spends_time, axiom, ! [X] : (born_multiple_birth(X) => spends_time_with_siblings(X))).
fof(siblings_born_together_born_multiple, axiom, ! [X] : (siblings_born_together(X) => born_multiple_birth(X))).
fof(complains_siblings_born_together, axiom, ! [X] : (complains_about_siblings(X) => siblings_born_together(X))).
fof(lives_at_home_not_strangers, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(spends_time_lives_at_home, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).
fof(luke_disjunction, axiom, (born_multiple_birth(luke) & lives_with_strangers(luke)) | (~born_multiple_birth(luke) & ~lives_with_strangers(luke))).
fof(goal, conjecture, ~(~born_multiple_birth(luke) & ~complains_about_siblings(luke))).