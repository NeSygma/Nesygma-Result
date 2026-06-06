% Negative version: negated claim as conjecture
fof(premise1, axiom, ! [X] : (multiple_birth(X) => spends_time_with_siblings(X))).
fof(premise2, axiom, ! [X] : (has_siblings_born_together(X) => multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains_about_siblings(X) => has_siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time_with_siblings(X) => lives_at_home(X))).
fof(premise6, axiom, (multiple_birth(luke) & lives_with_strangers(luke)) | (~multiple_birth(luke) & ~lives_with_strangers(luke))).
fof(conclusion, conjecture, ~spends_time_with_siblings(luke)).