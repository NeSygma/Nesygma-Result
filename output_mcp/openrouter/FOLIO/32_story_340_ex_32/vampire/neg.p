% Negative version
fof(premise1, axiom, ! [X] : (mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(premise2, axiom, ! [X] : ((mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).
fof(premise3, axiom, ! [X] : ((mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).
fof(premise4, axiom, ! [X] : ((mixer(X) & professional_tennis_player(X)) => athlete(X))).
fof(premise5, axiom, ! [X] : ((mixer(X) & celebrity(X)) => well_paid(X))).
fof(premise6, axiom, ! [X] : ((mixer(X) & athlete(X)) => famous(X))).
fof(premise7, axiom, ! [X] : ((mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(premise8, axiom, mixer(djokovic)).
fof(premise9, axiom, ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).
fof(goal, conjecture, ~lives_in_tax_haven(djokovic)).