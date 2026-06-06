fof(p1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(p2, axiom, ! [X] : ((grand_slam_champion(X) & at_mixer(X)) => professional_tennis_player(X))).
fof(p3, axiom, ! [X] : ((oscar_nominated_actor(X) & at_mixer(X)) => celebrity(X))).
fof(p4, axiom, ! [X] : ((professional_tennis_player(X) & at_mixer(X)) => athlete(X))).
fof(p5, axiom, ! [X] : ((celebrity(X) & at_mixer(X)) => well_paid(X))).
fof(p6, axiom, ! [X] : ((athlete(X) & at_mixer(X)) => famous(X))).
fof(p7, axiom, ! [X] : ((well_paid(X) & at_mixer(X)) => lives_in_tax_haven(X))).
fof(p8, axiom, at_mixer(djokovic)).
fof(p9, axiom, ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).
fof(goal, conjecture, ~lives_in_tax_haven(djokovic)).