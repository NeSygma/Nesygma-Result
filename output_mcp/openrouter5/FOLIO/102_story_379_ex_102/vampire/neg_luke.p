% Negative version: negated claim as conjecture
fof(premise1, axiom, ! [X] : (multiple_birth(X) => spends_time(X))).
fof(premise2, axiom, ! [X] : (has_siblings_together(X) => multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains(X) => has_siblings_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spends_time(X) => lives_at_home(X))).

fof(premise6, axiom, 
    ((baby_multiple_birth(luke) & lives_with_strangers(luke)) | (~baby_multiple_birth(luke) & ~lives_with_strangers(luke)))).

fof(baby_link, axiom, ! [X] : (baby_multiple_birth(X) => multiple_birth(X))).

fof(goal, conjecture, ~spends_time(luke)).