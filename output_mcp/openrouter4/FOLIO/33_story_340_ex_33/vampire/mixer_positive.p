% Positive file: check if "Djokovic does not live in a tax haven" is entailed
fof(premise1, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominee(X)))).
fof(premise2, axiom, ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => tennis_player(X))).
fof(premise3, axiom, ! [X] : ((at_mixer(X) & oscar_nominee(X)) => celebrity(X))).
fof(premise4, axiom, ! [X] : ((at_mixer(X) & tennis_player(X)) => athlete(X))).
fof(premise5, axiom, ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).
fof(premise6, axiom, ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).
fof(premise7, axiom, ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(premise8, axiom, at_mixer(djokovic) & ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).
fof(goal, conjecture, ~lives_in_tax_haven(djokovic)).