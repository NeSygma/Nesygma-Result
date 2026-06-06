fof(known_as_ailton, axiom, known_as(ailton_silva, ailton)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned_out_ailton, axiom, loaned_out(ailton, braga)).
fof(football_club_braga, axiom, football_club(braga)).
fof(football_player_ailton_silva, axiom, football_player(ailton_silva)).
fof(brazilian_ailton_silva, axiom, brazilian(ailton_silva)).
fof(plays_for_ailton_silva, axiom, plays_for(ailton_silva, nautico)).
fof(football_club_nautico, axiom, football_club(nautico)).
fof(football_club_fluminense, axiom, football_club(fluminense)).
fof(distinct_ailton_silva_ailton, axiom, ailton_silva != ailton).
fof(rule_known_loan, axiom, ! [A,B,C] : ((known_as(A,B) & loaned_out(B,C)) => loaned_out(A,C))).
fof(conjecture, conjecture, ? [X] : (loaned_out(ailton_silva, X) & football_club(X))).