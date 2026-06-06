fof(at_mixer_djokovic, axiom, at_mixer(djokovic)).
fof(everyone_mixer_gs_or_oscar, axiom,
    ! [X] : (at_mixer(X) => (grand_slam_champion(X) | oscar_nominated_actor(X)))).
fof(gs_champion_tennis_player, axiom,
    ! [X] : ((at_mixer(X) & grand_slam_champion(X)) => professional_tennis_player(X))).
fof(oscar_celebrity, axiom,
    ! [X] : ((at_mixer(X) & oscar_nominated_actor(X)) => celebrity(X))).
fof(tennis_player_athlete, axiom,
    ! [X] : ((at_mixer(X) & professional_tennis_player(X)) => athlete(X))).
fof(celebrity_well_paid, axiom,
    ! [X] : ((at_mixer(X) & celebrity(X)) => well_paid(X))).
fof(athlete_famous, axiom,
    ! [X] : ((at_mixer(X) & athlete(X)) => famous(X))).
fof(well_paid_tax_haven, axiom,
    ! [X] : ((at_mixer(X) & well_paid(X)) => lives_in_tax_haven(X))).
fof(djokovic_famous_athlete_implies_well_paid, axiom,
    ((famous(djokovic) & athlete(djokovic)) => well_paid(djokovic))).

fof(distinct_entities, axiom, djokovic != oscar_nominated_actor(djokovic)).

fof(conclusion_negation, conjecture, ~grand_slam_champion(djokovic)).