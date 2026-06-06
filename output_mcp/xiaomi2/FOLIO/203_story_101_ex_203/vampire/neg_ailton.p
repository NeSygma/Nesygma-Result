fof(common_name, axiom, ailton_silva = ailton).
fof(premise2, axiom, (football_player(ailton) & loaned_out_to(ailton, braga))).
fof(premise3, axiom, (brazilian(ailton_silva) & footballer(ailton_silva) & plays_for(ailton_silva, nautico))).
fof(premise4, axiom, (football_club(nautico) & football_club(braga))).
fof(premise5, axiom, football_club(fluminense)).
fof(goal, conjecture, ~ ? [X] : (loaned_out_to(ailton_silva, X) & football_club(X))).