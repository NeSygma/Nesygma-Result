fof(distinct, axiom, (ailton_silva != ailton & ailton_silva != nautico & ailton_silva != braga & ailton_silva != fluminense & ailton != nautico & ailton != braga & ailton != fluminense & nautico != braga & nautico != fluminense & braga != fluminense)).
fof(alias, axiom, alias(ailton_silva, ailton)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(played_ailton, axiom, played_for(ailton, braga)).
fof(brazilian, axiom, brazilian(ailton_silva)).
fof(football_player_ailton_silva, axiom, football_player(ailton_silva)).
fof(played_ailton_silva, axiom, played_for(ailton_silva, nautico)).
fof(club_nautico, axiom, club(nautico)).
fof(club_braga, axiom, club(braga)).
fof(club_fluminense, axiom, club(fluminense)).
fof(goal, conjecture, ~played_for(ailton_silva, fluminense)).