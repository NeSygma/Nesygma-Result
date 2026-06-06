fof(ailton_loaned_to_braga, axiom, loaned_to(ailton, braga)).
fof(braga_is_club, axiom, is_football_club(braga)).
fof(nautico_is_club, axiom, is_football_club(nautico)).
fof(fluminense_is_club, axiom, is_football_club(fluminense)).
fof(ailton_plays_for_nautico, axiom, plays_for(ailton, nautico)).
fof(conclusion, conjecture, ! [C] : (is_football_club(C) => ~loaned_to(ailton, C))).