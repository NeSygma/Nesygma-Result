fof(pos_axiom_1, axiom, football_player(ailton)).
fof(pos_axiom_2, axiom, loaned_out_to(ailton, braga)).
fof(pos_axiom_3, axiom, football_club(braga)).
fof(pos_axiom_4, axiom, football_club(nautico)).
fof(pos_axiom_5, axiom, football_club(fluminense)).
fof(pos_alias, axiom, (ailton_silva = ailton)).
fof(pos_conjecture, conjecture, ? [X] : (football_club(X) & loaned_out_to(ailton_silva, X))).