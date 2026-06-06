% Negative version
fof(eq_ailton, axiom, ailton_silva = ailton).
fof(brazilian_ailton, axiom, brazilian(ailton_silva)).
fof(plays_ailton, axiom, plays_for(ailton_silva, nautico)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned, axiom, loaned_out(ailton, braga)).
fof(club_braga, axiom, club(braga)).
fof(club_nautico, axiom, club(nautico)).
fof(club_fluminense, axiom, club(fluminense)).
fof(distinct_clubs, axiom, (braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ? [X] : (plays_for(X, nautico) & brazilian(X))).