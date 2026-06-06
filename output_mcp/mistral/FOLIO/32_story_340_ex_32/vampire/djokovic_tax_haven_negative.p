fof(at_mixer_def, axiom, ! [X] : (at_mixer(X) => (is_grand_slam_champion(X) | is_oscar_nominated_actor(X)))).
fof(gs_champion_to_tennis_player, axiom, ! [X] : ((at_mixer(X) & is_grand_slam_champion(X)) => is_professional_tennis_player(X))).
fof(oscar_actor_to_celebrity, axiom, ! [X] : ((at_mixer(X) & is_oscar_nominated_actor(X)) => is_celebrity(X))).
fof(tennis_player_to_athlete, axiom, ! [X] : ((at_mixer(X) & is_professional_tennis_player(X)) => is_athlete(X))).
fof(celebrity_to_well_paid, axiom, ! [X] : ((at_mixer(X) & is_celebrity(X)) => is_well_paid(X))).
fof(athlete_to_famous, axiom, ! [X] : ((at_mixer(X) & is_athlete(X)) => is_famous(X))).
fof(well_paid_to_tax_haven, axiom, ! [X] : ((at_mixer(X) & is_well_paid(X)) => lives_in_tax_haven(X))).
fof(djokovic_at_mixer, axiom, at_mixer(djokovic)).
fof(djokovic_famous_athlete_implies_well_paid, axiom, ((is_famous(djokovic) & is_athlete(djokovic)) => is_well_paid(djokovic))).
fof(goal, conjecture, ~lives_in_tax_haven(djokovic)).