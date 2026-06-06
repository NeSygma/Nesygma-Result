% Positive version: Conjecture is "Djokovic lives in a tax haven"
fof(premise_1, axiom, ! [X] :
    ( (person_at_mixer(X)) =>
      ( grand_slam_champion(X) | oscar_nominated_actor(X) ) )).

fof(premise_2, axiom, ! [X] :
    ( (grand_slam_champion(X) & person_at_mixer(X)) =>
      professional_tennis_player(X) )).

fof(premise_3, axiom, ! [X] :
    ( (oscar_nominated_actor(X) & person_at_mixer(X)) =>
      celebrity(X) )).

fof(premise_4, axiom, ! [X] :
    ( (professional_tennis_player(X) & person_at_mixer(X)) =>
      athlete(X) )).

fof(premise_5, axiom, ! [X] :
    ( (celebrity(X) & person_at_mixer(X)) =>
      well_paid(X) )).

fof(premise_6, axiom, ! [X] :
    ( (athlete(X) & person_at_mixer(X)) =>
      famous(X) )).

fof(premise_7, axiom, ! [X] :
    ( (well_paid(X) & person_at_mixer(X)) =>
      lives_in_tax_haven(X) )).

fof(premise_8, axiom,
    ( person_at_mixer(djokovic) &
      ( (famous(djokovic) & athlete(djokovic)) => well_paid(djokovic) ) )).

fof(goal, conjecture, lives_in_tax_haven(djokovic)).