fof(p1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(p2, axiom, ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).
fof(p3, axiom, ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).
fof(p4, axiom, ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).
fof(p5, axiom, ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).
fof(p6, axiom, ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).
fof(p7, axiom, ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(p8, axiom, at_mixer(djokovic) & ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).
fof(goal, conjecture, grand_slam_champion(djokovic)).