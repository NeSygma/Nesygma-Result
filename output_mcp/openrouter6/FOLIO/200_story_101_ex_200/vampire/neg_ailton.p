fof(born_1995, axiom, born_in_1995(ailton_silva)).
fof(known_as, axiom, known_as(ailton_silva, ailton)).
fof(football_player, axiom, football_player(ailton_silva)).
fof(loaned_to, axiom, loaned_to(ailton_silva, braga)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(club_nautico, axiom, football_club(nautico)).
fof(club_braga, axiom, football_club(braga)).
fof(club_fluminense, axiom, football_club(fluminense)).
fof(distinct_entities, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ? [C] : (football_club(C) & plays_for(ailton_silva, C))).