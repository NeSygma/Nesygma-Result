fof(ailton_silva_is_ailton, axiom, ailton_silva = ailton).
fof(ailton_plays_for_braga, axiom, plays_for(ailton, braga)).
fof(ailton_silva_is_brazilian_and_plays_for_nautico, axiom, is_brazilian(ailton_silva) & plays_for(ailton_silva, nautico)).
fof(nautico_and_braga_are_clubs, axiom, is_football_club(nautico) & is_football_club(braga)).
fof(fluminense_is_club, axiom, is_football_club(fluminense)).
fof(conclusion, conjecture, ! [X] : (plays_for(X, nautico) => ~is_brazilian(X))).