% Negative version: Negated claim as conjecture
fof(premise_1, axiom, ! [X] : (multiple_birth(X) => spend_time_with_siblings(X))).
fof(premise_2, axiom, ! [X] : (siblings_born_together(X) => multiple_birth(X))).
fof(premise_3, axiom, ! [X] : (complain_about_siblings(X) => siblings_born_together(X))).
fof(premise_4, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(premise_5, axiom, ! [X] : (spend_time_with_siblings(X) => live_at_home(X))).
fof(premise_6, axiom, (multiple_birth(luke) & live_with_strangers(luke)) | (~multiple_birth(luke) & ~live_with_strangers(luke))).
fof(goal_negation, conjecture, ~spend_time_with_siblings(luke)).