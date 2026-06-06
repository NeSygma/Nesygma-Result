% Positive version: claim that Djokovic does NOT live in a tax haven
fof(premise1, axiom, ! [X] : (grand_slam_champion(X) | oscar_nominated_actor(X))).
fof(premise2, axiom, ! [X] : (grand_slam_champion(X) => professional_tennis_player(X))).
fof(premise3, axiom, ! [X] : (oscar_nominated_actor(X) => celebrity(X))).
fof(premise4, axiom, ! [X] : (professional_tennis_player(X) => athlete(X))).
fof(premise5, axiom, ! [X] : (celebrity(X) => well_paid(X))).
fof(premise6, axiom, ! [X] : (athlete(X) => famous(X))).
fof(premise7, axiom, ! [X] : (well_paid(X) => live_in_tax_haven(X))).
fof(premise8, axiom, (famous(djokovic) & athlete(djokovic)) => well_paid(djokovic)).
fof(goal, conjecture, ~live_in_tax_haven(djokovic)).