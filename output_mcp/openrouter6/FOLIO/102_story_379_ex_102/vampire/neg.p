fof(premise1, axiom, ! [X] : (multiple_birth(X) => spend_time(X))).
fof(premise2, axiom, ! [X] : (siblings_born_together(X) => multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complain_about_siblings(X) => siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spend_time(X) => live_at_home(X))).
fof(premise6, axiom, (multiple_birth(luke) & live_with_strangers(luke)) | (~multiple_birth(luke) & ~live_with_strangers(luke))).
fof(goal, conjecture, ~spend_time(luke)).