fof(born_in_ailton_silva, axiom, born_in(ailton_silva, year_1995)).
fof(commonly_known_as_ailton_silva, axiom, commonly_known_as(ailton_silva, ailton)).
fof(is_football_player_ailton_silva, axiom, is_football_player(ailton_silva)).
fof(loaned_to_ailton_silva_braga, axiom, loaned_to(ailton_silva, braga)).
fof(plays_for_ailton_silva_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(is_football_club_braga, axiom, is_football_club(braga)).
fof(is_football_club_nautico, axiom, is_football_club(nautico)).
fof(is_football_club_fluminense, axiom, is_football_club(fluminense)).
fof(distinct_entities, axiom, ailton_silva != ailton & ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense).
fof(conclusion, conjecture, ~(? [C] : plays_for(ailton_silva, C))).