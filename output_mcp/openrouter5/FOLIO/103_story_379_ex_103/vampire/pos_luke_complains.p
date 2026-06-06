% Positive version: Conjecture is "Luke complains often about annoying siblings"
% Predicates:
% multiple_birth_siblings(X) - X is born in a multiple birth with siblings
% spend_time_siblings(X) - X spends a lot of time hanging out with and playing with their siblings
% siblings_born_together(X) - X has siblings who were born together
% complain_annoying(X) - X complains often about annoying siblings
% live_at_home(X) - X lives at home
% live_with_strangers(X) - X lives with strangers
% baby_multiple_birth(X) - X is a baby born in a multiple birth

fof(premise1, axiom, ! [X] : (multiple_birth_siblings(X) => spend_time_siblings(X))).
fof(premise2, axiom, ! [X] : (siblings_born_together(X) => multiple_birth_siblings(X))).
fof(premise3, axiom, ! [X] : (complain_annoying(X) => siblings_born_together(X))).
fof(premise4, axiom, ! [X] : (live_at_home(X) => ~live_with_strangers(X))).
fof(premise5, axiom, ! [X] : (spend_time_siblings(X) => live_at_home(X))).
fof(premise6, axiom, 
    ( (baby_multiple_birth(luke) & live_with_strangers(luke)) 
    | (~baby_multiple_birth(luke) & ~live_with_strangers(luke)) )).

fof(goal, conjecture, complain_annoying(luke)).