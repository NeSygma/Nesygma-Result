fof(multiple_birth_sibling_def, axiom, ! [X] : (multiple_birth_sibling(X) => hang_out_with_siblings(X))).
fof(born_together_siblings_def, axiom, ! [X] : (born_together_siblings(X) => multiple_birth_sibling(X))).
fof(complain_annoying_siblings_def, axiom, ! [X] : (complain_annoying_siblings(X) => born_together_siblings(X))).
fof(live_at_home_def, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(hang_out_with_siblings_def, axiom, ! [X] : (hang_out_with_siblings(X) => live_at_home(X))).
fof(luke_alternative, axiom, (multiple_birth_sibling(luke) & live_with_strangers(luke)) | (~multiple_birth_sibling(luke) & ~live_with_strangers(luke))).

fof(goal, conjecture, hang_out_with_siblings(luke)).