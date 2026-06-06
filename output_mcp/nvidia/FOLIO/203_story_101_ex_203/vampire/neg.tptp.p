fof(neg_axiom_1, axiom, football_player(ailton)).
fof(neg_axiom_2, axiom, loaned_out_to(ailton, braga)).
fof(neg_axiom_3, axiom, football_club(braga)).
fof(neg_axiom_4, axiom, football_club(nautico)).
fof(neg_axiom_5, axiom, football_club(fluminense)).
fof(neg_alias, axiom, (ailton_silva = ailton)).
fof(neg_conjecture, conjecture, ~ ? [X] : (football_club(X) & loaned_out_to(ailton_silva, X))).