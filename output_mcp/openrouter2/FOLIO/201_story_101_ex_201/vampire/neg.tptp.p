fof(equality, axiom, ailton_silva = ailton).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned_to_braga, axiom, loaned_out_to(ailton, braga)).
fof(brazilian_ailton, axiom, brazilian(ailton_silva)).
fof(plays_for_ailton, axiom, plays_for(ailton_silva, nautico)).
fof(football_club_braga, axiom, football_club(braga)).
fof(football_club_nautico, axiom, football_club(nautico)).
fof(football_club_fluminense, axiom, football_club(fluminense)).
fof(conjecture, conjecture, ? [Y] : (football_club(Y) & loaned_out_to(ailton, Y))).