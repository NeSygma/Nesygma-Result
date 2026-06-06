fof(ailton_silva_is_ailton, axiom, (ailton_silva = ailton)).
fof(ailton_is_football_player, axiom, is_football_player(ailton)).
fof(ailton_loaned_to_braga, axiom, loaned_to(ailton, braga)).
fof(braga_is_football_club, axiom, is_football_club(braga)).
fof(nautico_is_football_club, axiom, is_football_club(nautico)).
fof(fluminense_is_football_club, axiom, is_football_club(fluminense)).
fof(ailton_silva_plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(goal, conjecture, ? [C] : (is_football_club(C) & loaned_to(ailton_silva, C))).