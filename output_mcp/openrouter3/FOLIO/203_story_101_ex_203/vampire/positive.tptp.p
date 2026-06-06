fof(distinct_entities, axiom, (ailton_silva != ailton & ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & ailton != braga & ailton != nautico & ailton != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(nickname, axiom, nickname(ailton_silva, ailton)).
fof(football_player, axiom, football_player(ailton)).
fof(loaned_to_braga, axiom, loaned_to(ailton, braga)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(club_braga, axiom, football_club(braga)).
fof(club_nautico, axiom, football_club(nautico)).
fof(club_fluminense, axiom, football_club(fluminense)).
fof(goal, conjecture, ? [X] : (football_club(X) & loaned_to(ailton_silva, X))).