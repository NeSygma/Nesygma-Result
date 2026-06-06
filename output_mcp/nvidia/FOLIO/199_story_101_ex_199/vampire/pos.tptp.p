fof(known_as_ailton, axiom, known_as(ailton, ailton_silva)).
fof(born_in_fact, axiom, born_in(ailton_silva, year_1995)).
fof(player_ailton, axiom, player(ailton)).
fof(player_ailton_silva, axiom, player(ailton_silva)).
fof(loaned_to_braga, axiom, loaned_to(ailton, braga)).
fof(brazilian_ailton_silva, axiom, brazilian(ailton_silva)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(football_club_nautico, axiom, football_club(nautico)).
fof(football_club_braga, axiom, football_club(braga)).
fof(football_club_fluminense, axiom, football_club(fluminense)).
fof(conclusion, conjecture, ! [X] : (plays_for(X, nautico) => ~brazilian(X))).