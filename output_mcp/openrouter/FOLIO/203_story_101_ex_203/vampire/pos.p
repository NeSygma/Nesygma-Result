% Positive version
fof(eq_name, axiom, ailton_silva = ailton).
fof(loaned, axiom, loaned_out(ailton, braga)).
fof(fc_braga, axiom, football_club(braga)).
fof(fc_nautico, axiom, football_club(nautico)).
fof(fc_fluminense, axiom, football_club(fluminense)).
fof(play, axiom, plays_for(ailton_silva, nautico)).
fof(conj, conjecture, ? [C] : (loaned_out(ailton_silva, C) & football_club(C))).