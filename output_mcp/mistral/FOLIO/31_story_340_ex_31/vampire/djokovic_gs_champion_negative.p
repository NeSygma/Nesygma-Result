fof(at_mixer_def, axiom, ! [P] : (at_mixer(P) => (grand_slam_champion(P) | oscar_nominated_actor(P))) ).
fof(gs_champion_to_tennis_player, axiom, ! [P] : ((at_mixer(P) & grand_slam_champion(P)) => professional_tennis_player(P)) ).
fof(oscar_actor_to_celebrity, axiom, ! [P] : ((at_mixer(P) & oscar_nominated_actor(P)) => celebrity(P)) ).
fof(tennis_player_to_athlete, axiom, ! [P] : ((at_mixer(P) & professional_tennis_player(P)) => athlete(P)) ).
fof(celebrity_to_well_paid, axiom, ! [P] : ((at_mixer(P) & celebrity(P)) => well_paid(P)) ).
fof(athlete_to_famous, axiom, ! [P] : ((at_mixer(P) & athlete(P)) => famous(P)) ).
fof(well_paid_to_tax_haven, axiom, ! [P] : ((at_mixer(P) & well_paid(P)) => lives_in_tax_haven(P)) ).
fof(djokovic_at_mixer, axiom, at_mixer(djokovic) ).
fof(djokovic_famous_athlete_implies_well_paid, axiom, (athlete(djokovic) => well_paid(djokovic)) ).
fof(goal_negation, conjecture, ~grand_slam_champion(djokovic) ).