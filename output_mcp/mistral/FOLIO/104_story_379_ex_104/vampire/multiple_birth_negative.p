fof(multiple_birth_implies_spend_time, axiom, ! [X] : (multiple_birth(X) => spend_time_with_siblings(X))).
fof(siblings_born_together_implies_multiple, axiom, ! [X] : (siblings_born_together(X) => multiple_birth(X))).
fof(complains_implies_siblings_born_together, axiom, ! [X] : (complains_about_siblings(X) => siblings_born_together(X))).
fof(lives_at_home_implies_not_strangers, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(spend_time_implies_lives_at_home, axiom, ! [X] : (spend_time_with_siblings(X) => lives_at_home(X))).
fof(luke_alternative, axiom, (multiple_birth(luke) & lives_with_strangers(luke)) | (~multiple_birth(luke) & ~lives_with_strangers(luke))).

fof(conclusion_negation, conjecture, (multiple_birth(luke) | complains_about_siblings(luke))).