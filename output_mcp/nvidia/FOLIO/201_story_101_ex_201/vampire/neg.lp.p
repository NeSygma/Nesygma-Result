fof(loaned_to_braga, axiom, loaned_out_to(ailton, braga)).
fof(club_braga, axiom, club(braga)).
fof(club_nau, axiom, club(nau_tico)).
fof(club_fluminense, axiom, club(fluminense)).
fof(neg_conclusion, conjecture, ? [X] : (club(X) & loaned_out_to(ailton, X))).