fof(born_in_ailton_silva, axiom, born_in(ailton_silva, year_1995)).
fof(known_as_ailton, axiom, known_as(ailton_silva, ailton)).
fof(is_football_player_ailton, axiom, is_football_player(ailton)).
fof(loaned_to_ailton_braga, axiom, loaned_to(ailton, braga)).
fof(plays_for_ailton_nautico, axiom, plays_for(ailton, nautico)).
fof(is_brazilian_ailton, axiom, is_brazilian(ailton)).
fof(is_club_braga, axiom, is_club(braga)).
fof(is_club_nautico, axiom, is_club(nautico)).
fof(is_club_fluminense, axiom, is_club(fluminense)).
fof(club_nautico_braga, axiom, nautico != braga).
fof(club_nautico_fluminense, axiom, nautico != fluminense).
fof(club_braga_fluminense, axiom, braga != fluminense).

fof(negated_conclusion, conjecture, ? [X] : (plays_for(X, nautico) & is_brazilian(X))).