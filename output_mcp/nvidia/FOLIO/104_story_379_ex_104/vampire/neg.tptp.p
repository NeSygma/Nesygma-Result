fof(born_multiple_birth_implies_spend, axiom, ! [X] : (born_in_multiple_birth(X) => spend_time_with_siblings(X))).
fof(has_sibling_born_together_implies_born_multiple_birth, axiom, ! [X] : (has_sibling_born_together(X) => born_in_multiple_birth(X))).
fof(complains_about_annoying_siblings_implies_has_sibling_born_together, axiom, ! [X] : (complains_about_annoying_siblings(X) => has_sibling_born_together(X))).
fof(lives_at_home_implies_not_lives_with_strangers, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(spend_time_with_siblings_implies_lives_at_home, axiom, ! [X] : (spend_time_with_siblings(X) => lives_at_home(X))).
fof(luke_choice, axiom, (born_in_multiple_birth(luke) & lives_with_strangers(luke)) | ( ~born_in_multiple_birth(luke) & ~lives_with_strangers(luke) )).
fof(neg_conclusion, conjecture, born_in_multiple_birth(luke) | complains_about_annoying_siblings(luke)).