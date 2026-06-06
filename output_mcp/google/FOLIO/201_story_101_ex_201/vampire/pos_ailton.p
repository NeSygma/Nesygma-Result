fof(ailton_silva_is_ailton, axiom, is_known_as(ailton_silva, ailton)).
fof(ailton_loaned_to_braga, axiom, loaned_to(ailton_silva, braga)).
fof(braga_is_club, axiom, is_football_club(braga)).
fof(nautico_is_club, axiom, is_football_club(nautico)).
fof(fluminense_is_club, axiom, is_football_club(fluminense)).
fof(distinct_entities, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ~ ? [C] : (loaned_to(ailton_silva, C) & is_football_club(C))).