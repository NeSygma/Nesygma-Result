fof(p1, axiom, ! [X] : (likes_music(X) => wants_to_compose(X))).
fof(p2, axiom, ! [X] : (has_access_program(X) => can_compose(X))).
fof(p3, axiom, ! [X] : ((can_compose(X) & wants_to_compose(X)) => will_compose(X))).
fof(goal_neg, conjecture, ~(! [X] : ((likes_music(X) & has_access_program(X)) => will_compose(X)))).