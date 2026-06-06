fof(premise_1, axiom, ! [X] : (likes_music(X) => wants_to_compose(X))).
fof(premise_2, axiom, ! [X] : (has_access_to_program(X) => can_compose(X))).
fof(premise_3, axiom, ! [X] : ((can_compose(X) & wants_to_compose(X)) => will_compose(X))).
fof(goal, conjecture, ! [X] : ((likes_music(X) & has_access_to_program(X)) => will_compose(X))).