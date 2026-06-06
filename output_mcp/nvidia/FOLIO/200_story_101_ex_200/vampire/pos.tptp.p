fof(alias_def, axiom, alias(ailton_silva, ailton)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned_to_brag, axiom, loaned_to(ailton, brag)).
fof(brazilian_ailton_silva, axiom, brazilian(ailton_silva)).
fof(footballer_ailton_silva, axiom, footballer(ailton_silva)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(football_club_nautico, axiom, football_club(nautico)).
fof(football_club_brag, axiom, football_club(brag)).
fof(football_club_fluminense, axiom, football_club(fluminense)).
fof(conclusion, conjecture, ~? [X] : (football_club(X) & plays_for(ailton_silva, X))).