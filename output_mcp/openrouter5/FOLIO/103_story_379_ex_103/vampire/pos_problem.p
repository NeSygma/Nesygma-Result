% Positive version: Conjecture is "Luke complains often about annoying siblings"
% Predicates:
% multiple_birth_siblings(X) - X is born in a multiple birth with siblings
% hangs_out_plays(X) - X spends a lot of time hanging out with and playing with their siblings
% siblings_born_together(X) - X has siblings who were born together
% complains_annoying(X) - X complains often about annoying siblings
% lives_at_home(X) - X lives at home
% lives_with_strangers(X) - X lives with strangers
% baby_multiple_birth(X) - X is a baby born in a multiple birth

fof(premise1, axiom, ! [X] : (multiple_birth_siblings(X) => hangs_out_plays(X))).
fof(premise2, axiom, ! [X] : (siblings_born_together(X) => multiple_birth_siblings(X))).
fof(premise3, axiom, ! [X] : (complains_annoying(X) => siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (hangs_out_plays(X) => lives_at_home(X))).
fof(premise6, axiom, 
    ( (baby_multiple_birth(luke) & lives_with_strangers(luke)) | 
      (~baby_multiple_birth(luke) & ~lives_with_strangers(luke)) )).

fof(goal, conjecture, complains_annoying(luke)).