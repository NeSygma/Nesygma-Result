fof(at_mixer_djokovic, axiom, at_mixer(djokovic)).
fof(rule_everyone, axiom, ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(rule_gs_to_ptp, axiom, ! [X] : (at_mixer(X) & grand_slam_champion(X) => professional_tennis_player(X))).
fof(rule_ptp_to_athlete, axiom, ! [X] : (at_mixer(X) & professional_tennis_player(X) => athlete(X))).
fof(rule_oscar_to_celebrity, axiom, ! [X] : (at_mixer(X) & oscar_nominated_actor(X) => celebrity(X))).
fof(rule_celebrity_to_well_paid, axiom, ! [X] : (at_mixer(X) & celebrity(X) => well_paid(X))).
fof(rule_athlete_to_famous, axiom, ! [X] : (at_mixer(X) & athlete(X) => famous(X))).
fof(rule_well_paid_to_tax_haven, axiom, ! [X] : (at_mixer(X) & well_paid(X) => live_in_tax_haven(X))).
fof(rule_djokovic_conditional, axiom, (famous(djokovic) & athlete(djokovic)) => well_paid(djokovic)).
fof(conjecture, conjecture, grand_slam_champion(djokovic)).