fof(distinct_entities, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & ailton != braga & ailton != nautico & ailton != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).

fof(ailton_is_ailton_silva, axiom, ailton = ailton_silva).

fof(ailton_football_player, axiom, football_player(ailton)).

fof(ailton_loaned_to_braga, axiom, loaned_to(ailton, braga)).

fof(ailton_silva_brazilian, axiom, brazilian(ailton_silva)).

fof(ailton_silva_plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).

fof(nautico_football_club, axiom, football_club(nautico)).

fof(braga_football_club, axiom, football_club(braga)).

fof(fluminense_football_club, axiom, football_club(fluminense)).

fof(goal, conjecture, ! [X] : (plays_for(X, nautico) => ~brazilian(X))).