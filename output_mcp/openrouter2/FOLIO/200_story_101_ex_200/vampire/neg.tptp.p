fof(alias, axiom, alias(ailton_silva, ailton)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned_to, axiom, loaned_to(ailton, braga)).
fof(football_player_ailton_silva, axiom, football_player(ailton_silva)).
fof(brazilian, axiom, brazilian(ailton_silva)).
fof(plays_for, axiom, plays_for(ailton_silva, nautico)).
fof(football_club_nautico, axiom, football_club(nautico)).
fof(football_club_braga, axiom, football_club(braga)).
fof(football_club_fluminense, axiom, football_club(fluminense)).
fof(distinctness, axiom, (ailton_silva != ailton & ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & ailton != braga & ailton != nautico & ailton != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ? [C] : (football_club(C) & plays_for(ailton_silva, C))).