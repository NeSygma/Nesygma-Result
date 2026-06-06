fof(at_mixer_premise, axiom, at_mixer(djokovic)).
fof(everyone_at_mixer_is_champion_or_actor, axiom,
    ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(grand_slam_champion_implies_tennis_player, axiom,
    ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).
fof(oscar_nominated_actor_implies_celebrity, axiom,
    ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).
fof(tennis_player_implies_athlete, axiom,
    ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).
fof(celebrity_implies_well_paid, axiom,
    ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).
fof(athlete_implies_famous, axiom,
    ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).
fof(well_paid_implies_tax_haven, axiom,
    ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(djokovic_famous_athlete_implies_well_paid, axiom,
    ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).

fof(negated_conclusion, conjecture, ~lives_in_tax_haven(djokovic)).