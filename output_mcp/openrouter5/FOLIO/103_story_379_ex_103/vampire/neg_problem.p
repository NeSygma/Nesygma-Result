% Negative version: Conjecture is "Luke does NOT complain often about annoying siblings"
fof(premise1, axiom, ! [X] : (multiple_birth_siblings(X) => hangs_out_plays(X))).
fof(premise2, axiom, ! [X] : (siblings_born_together(X) => multiple_birth_siblings(X))).
fof(premise3, axiom, ! [X] : (complains_annoying(X) => siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (hangs_out_plays(X) => lives_at_home(X))).
fof(premise6, axiom, 
    ( (baby_multiple_birth(luke) & lives_with_strangers(luke)) | 
      (~baby_multiple_birth(luke) & ~lives_with_strangers(luke)) )).

fof(goal, conjecture, ~complains_annoying(luke)).