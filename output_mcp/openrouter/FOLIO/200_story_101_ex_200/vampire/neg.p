% Negative conjecture: Ailton Silva plays for some football club
fof(distinct_entities, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(club_braga, axiom, club(braga)).
fof(club_nautico, axiom, club(nautico)).
fof(club_fluminense, axiom, club(fluminense)).
fof(plays_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(loaned_braga, axiom, loaned_to(ailton_silva, braga)).
fof(football_player, axiom, football_player(ailton_silva)).
fof(born_1995, axiom, born(ailton_silva, 1995)).
fof(known_as_ailton, axiom, known_as(ailton_silva, ailton)).
fof(brazilian, axiom, brazilian(ailton_silva)).
fof(goal, conjecture, ? [C] : (club(C) & plays_for(ailton_silva, C))).