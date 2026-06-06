fof(at_mixer_djokovic, axiom, at_mixer(djokovic)).
fof(djokovic_famous_athlete_implies_well_paid, axiom, ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).
fof(at_mixer_implies_gs_or_oscar, axiom, ![X] : ((at_mixer(X)) => ((grand_slam_champion(X) | oscar_nominated_actor(X))))).
fof(gs_champion_at_mixer_implies_ptp, axiom, ![X] : ((grand_slam_champion(X) & at_mixer(X)) => professional_tennis_player(X))).
fof(oscar_actor_at_mixer_implies_celebrity, axiom, ![X] : ((oscar_nominated_actor(X) & at_mixer(X)) => celebrity(X))).
fof(ptp_at_mixer_implies_athlete, axiom, ![X] : ((professional_tennis_player(X) & at_mixer(X)) => athlete(X))).
fof(athlete_at_mixer_implies_famous, axiom, ![X] : ((athlete(X) & at_mixer(X)) => famous(X))).
fof(celebrity_at_mixer_implies_well_paid, axiom, ![X] : ((celebrity(X) & at_mixer(X)) => well_paid(X))).
fof(well_paid_at_mixer_implies_live_in_tax_haven, axiom, ![X] : ((well_paid(X) & at_mixer(X)) => live_in_tax_haven(X))).
fof(conjecture, conjecture, live_in_tax_haven(djokovic)).