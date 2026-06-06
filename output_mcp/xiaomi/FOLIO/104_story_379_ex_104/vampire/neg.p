fof(premise1, axiom, ! [X] : (born_multiple(X) => spends_time_with_siblings(X))).
fof(premise2, axiom, ! [X] : (has_siblings_born_together(X) => born_multiple(X))).
fof(premise3, axiom, ! [X] : (complains_about_siblings(X) => has_siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).
fof(premise6, axiom, ((born_multiple(luke) & lives_with_strangers(luke)) | (~born_multiple(luke) & ~lives_with_strangers(luke)))).
fof(goal, conjecture, ~(~born_multiple(luke) & ~complains_about_siblings(luke))).