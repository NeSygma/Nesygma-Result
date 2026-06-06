% Positive version: Ailton Silva played for Fluminense
fof(distinct_entities, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(person_ailton_silva, axiom, person(ailton_silva)).
fof(club_braga, axiom, football_club(braga)).
fof(club_nautico, axiom, football_club(nautico)).
fof(club_fluminense, axiom, football_club(fluminense)).
fof(nickname_ailton, axiom, nickname(ailton, ailton_silva)).
fof(loaned_to_braga, axiom, loaned_to(ailton_silva, braga)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(goal, conjecture, plays_for(ailton_silva, fluminense)).