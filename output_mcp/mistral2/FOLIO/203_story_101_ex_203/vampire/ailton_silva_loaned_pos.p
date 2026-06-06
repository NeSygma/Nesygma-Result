fof(alias_ailton, axiom, alias(ailton, ailton_silva)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned_to_braga, axiom, loaned_out_to(ailton, braga)).
fof(football_player_ailton_silva, axiom, football_player(ailton_silva)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(football_club_nautico, axiom, football_club(nautico)).
fof(football_club_braga, axiom, football_club(braga)).
fof(football_club_fluminense, axiom, football_club(fluminense)).
fof(conclusion, conjecture, ? [Club] : loaned_out_to(ailton_silva, Club)).