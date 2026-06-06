% Positive version
fof(distinct_consts, axiom, (ailton_silva != ailton & ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & ailton != braga & ailton != nautico & ailton != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(equality, axiom, ailton_silva = ailton).
fof(fb_player1, axiom, football_player(ailton)).
fof(loaned, axiom, loaned_to(ailton, braga)).
fof(brazilian, axiom, brazilian(ailton_silva)).
fof(fb_player2, axiom, football_player(ailton_silva)).
fof(plays_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(club_braga, axiom, club(braga)).
fof(club_nautico, axiom, club(nautico)).
fof(club_fluminense, axiom, club(fluminense)).
fof(goal, conjecture, plays_for(ailton_silva, fluminense)).