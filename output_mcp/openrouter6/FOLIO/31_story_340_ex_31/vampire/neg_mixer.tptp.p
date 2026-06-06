fof(at_mixer_djokovic, axiom, at_mixer(djokovic)).
fof(premise_1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(premise_2, axiom, ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).
fof(premise_3, axiom, ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).
fof(premise_4, axiom, ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).
fof(premise_5, axiom, ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).
fof(premise_6, axiom, ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).
fof(premise_7, axiom, ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(premise_8a, axiom, at_mixer(djokovic)).
fof(premise_8b, axiom, (famous(djokovic) & athlete(djokovic)) => well_paid(djokovic)).
fof(goal, conjecture, ~grand_slam_champion(djokovic)).