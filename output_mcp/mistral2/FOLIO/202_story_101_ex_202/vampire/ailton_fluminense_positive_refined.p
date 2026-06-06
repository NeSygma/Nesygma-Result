fof(also_known_as_ailton, axiom, also_known_as(ailton_silva, ailton)).
fof(ailton_is_football_player, axiom, football_player(ailton_silva)).
fof(loaned_to_braga, axiom, loaned_to(ailton_silva, braga)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(braga_is_club, axiom, football_club(braga)).
fof(nautico_is_club, axiom, football_club(nautico)).
fof(fluminense_is_club, axiom, football_club(fluminense)).
fof(distinct_braga_nautico, axiom, braga != nautico).
fof(distinct_braga_fluminense, axiom, braga != fluminense).
fof(distinct_nautico_fluminense, axiom, nautico != fluminense).
fof(conclusion, conjecture, plays_for(ailton_silva, fluminense)).