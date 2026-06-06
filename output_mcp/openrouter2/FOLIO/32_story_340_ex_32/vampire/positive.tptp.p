fof(at_mixer_djokovic, axiom, at_mixer(djokovic)).
fof(rule1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(rule2, axiom, ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).
fof(rule3, axiom, ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).
fof(rule4, axiom, ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).
fof(rule5, axiom, ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).
fof(rule6, axiom, ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).
fof(rule7, axiom, ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(rule8, axiom, (famous(djokovic) & athlete(djokovic)) => well_paid(djokovic)).
fof(conjecture, conjecture, lives_in_tax_haven(djokovic)).